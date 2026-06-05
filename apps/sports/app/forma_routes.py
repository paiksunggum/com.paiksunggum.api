from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db

from apps.admin.app.controllers.ad_stats_daily_controller import AdStatsDailyController
from apps.admin.app.controllers.ads_controller import AdsController
from apps.admin.app.controllers.practice_controller import PracticeController
from apps.admin.app.controllers.sports_controller import SportsController
from apps.admin.app.controllers.users_ad_controller import UsersAdController
from apps.admin.app.schemas.ad_stats_daily_schema import (
    AdStatsDailyNestedCreateRequest,
    AdStatsDailyResponse,
)
from apps.admin.app.schemas.ads_schema import AdCreateRequest, AdResponse
from apps.admin.app.schemas.practice_schema import PracticeCreateRequest, PracticeResponse
from apps.admin.app.schemas.sports_schema import SportCreateRequest, SportResponse
from apps.admin.app.schemas.users_ad_schema import UsersAdNestedCreateRequest, UsersAdResponse
from apps.vision.app.controllers.analysis_history_controller import AnalysisHistoryController
from apps.vision.app.controllers.feedback_comments_controller import FeedbackCommentController
from apps.vision.app.controllers.feedback_controller import FeedbackController
from apps.vision.app.controllers.frame_controller import FrameController
from apps.vision.app.schemas.analysis_history_schema import (
    AnalysisHistoryResponse,
    AnalysisHistoryStartRequest,
    AnalysisHistoryUpdateRequest,
)
from apps.vision.app.schemas.feedback_comments_schema import (
    FeedbackCommentNestedCreateRequest,
    FeedbackCommentResponse,
)
from apps.vision.app.schemas.feedback_schema import FeedbackNestedCreateRequest, FeedbackResponse
from apps.vision.app.schemas.frame_schema import FrameNestedCreateRequest, FrameResponse

from .controllers.ad_link_controller import AdLinkController
from .controllers.payment_logs_controller import PaymentLogController
from .controllers.subscription_plans_controller import SubscriptionPlansController
from .controllers.subscriptions_controller import SubscriptionsController
from .controllers.user_skills_controller import UserSkillController
from .controllers.users_controller import UsersController
from .controllers.video_controller import VideoController
from .controllers.video_practice_match_controller import VideoPracticeMatchController
from .schemas.ad_link_schema import AdExposureCreateRequest, AdLinkResponse
from .schemas.payment_logs_schema import (
    PaymentLogNestedCreateRequest,
    PaymentLogResponse,
)
from .schemas.subscription_plans_schema import (
    SubscriptionPlanCreateRequest,
    SubscriptionPlanResponse,
)
from .schemas.subscriptions_schema import (
    SubscriptionNestedCreateRequest,
    SubscriptionResponse,
)
from .schemas.user_skills_schema import UserSkillNestedCreateRequest, UserSkillResponse
from .schemas.users_schema import FormaUserCreateRequest, FormaUserResponse
from .schemas.video_practice_match_schema import (
    VideoPracticeMatchNestedCreateRequest,
    VideoPracticeMatchResponse,
)
from .schemas.video_schema import VideoCreateRequest, VideoResponse

router = APIRouter(prefix="/forma", tags=["forma"])


def _integrity(detail: str = "제약 조건 위반입니다.") -> HTTPException:
    return HTTPException(status_code=400, detail=detail)


def _not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=404, detail=detail)


# --- Users (Secom shared) ---


@router.post("/users", response_model=FormaUserResponse)
async def forma_create_user(
    req: FormaUserCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        user = await UsersController(db).create_user(req)
        return FormaUserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.") from e
    except OperationalError as e:
        await db.rollback()
        raise HTTPException(
            status_code=503,
            detail="데이터베이스 연결에 실패했습니다. 잠시 후 다시 시도해 주세요.",
        ) from e
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e.orig or e)) from e


# --- Sports master ---


@router.get("/sports", response_model=list[SportResponse])
async def forma_list_sports(db: AsyncSession = Depends(get_db)):
    rows = await SportsController(db).list_sports()
    return [SportResponse.model_validate(r) for r in rows]


@router.post("/sports", response_model=SportResponse)
async def forma_create_sport(
    req: SportCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await SportsController(db).create_sport(req)
        return SportResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("중복되었거나 제약 조건 위반입니다.") from None


# --- Practice catalog ---


@router.get("/practices", response_model=list[PracticeResponse])
async def forma_list_practices(
    sport_id: int | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    rows = await PracticeController(db).list_practices(sport_id)
    return [PracticeResponse.model_validate(r) for r in rows]


@router.post("/practices", response_model=PracticeResponse)
async def forma_create_practice(
    req: PracticeCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await PracticeController(db).create_practice(req)
        return PracticeResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 sports id가 없거나 제약 조건 위반입니다.") from None


# --- Videos ---


@router.post("/videos", response_model=VideoResponse)
async def forma_create_video(
    req: VideoCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await VideoController(db).create_video(req)
        return VideoResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 user/sports id가 없거나 제약 조건 위반입니다.") from None


@router.get("/videos", response_model=list[VideoResponse])
async def forma_list_videos(
    user_id: int = Query(..., description="업로드한 사용자 id"),
    db: AsyncSession = Depends(get_db),
):
    rows = await VideoController(db).list_videos_by_user(user_id)
    return [VideoResponse.model_validate(r) for r in rows]


# --- Analysis history (nested under video) ---


@router.post(
    "/videos/{video_id}/analysis-history",
    response_model=AnalysisHistoryResponse,
)
async def forma_start_analysis_history(
    video_id: int,
    req: AnalysisHistoryStartRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await AnalysisHistoryController(db).start_for_video(video_id, req)
        return AnalysisHistoryResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 video_id가 없거나 제약 조건 위반입니다.") from None


@router.get(
    "/videos/{video_id}/analysis-history",
    response_model=list[AnalysisHistoryResponse],
)
async def forma_list_analysis_history_by_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
):
    rows = await AnalysisHistoryController(db).list_by_video(video_id)
    return [AnalysisHistoryResponse.model_validate(r) for r in rows]


@router.patch(
    "/analysis-history/{history_id}",
    response_model=AnalysisHistoryResponse,
)
async def forma_update_analysis_history(
    history_id: int,
    req: AnalysisHistoryUpdateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await AnalysisHistoryController(db).update_history(history_id, req)
        return AnalysisHistoryResponse.model_validate(row)
    except ValueError as e:
        raise _not_found(str(e)) from e


# --- Frames (nested under analysis history) ---


@router.post(
    "/analysis-history/{history_id}/frames",
    response_model=FrameResponse,
)
async def forma_create_frame(
    history_id: int,
    req: FrameNestedCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await FrameController(db).create_for_history(history_id, req)
        return FrameResponse.model_validate(row)
    except ValueError as e:
        raise _not_found(str(e)) from e
    except IntegrityError:
        await db.rollback()
        raise _integrity("제약 조건 위반입니다.") from None


@router.get(
    "/analysis-history/{history_id}/frames",
    response_model=list[FrameResponse],
)
async def forma_list_frames_by_history(
    history_id: int,
    db: AsyncSession = Depends(get_db),
):
    rows = await FrameController(db).list_by_history(history_id)
    return [FrameResponse.model_validate(r) for r in rows]


# --- Feedback (nested under video) ---


@router.get(
    "/videos/{video_id}/feedbacks",
    response_model=list[FeedbackResponse],
)
async def forma_list_feedbacks_by_video(
    video_id: int,
    db: AsyncSession = Depends(get_db),
):
    rows = await FeedbackController(db).list_by_video(video_id)
    return [FeedbackResponse.model_validate(r) for r in rows]


@router.post(
    "/videos/{video_id}/feedbacks",
    response_model=FeedbackResponse,
)
async def forma_create_feedback(
    video_id: int,
    req: FeedbackNestedCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await FeedbackController(db).create_for_video(video_id, req)
        return FeedbackResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 video/frame id가 없거나 제약 조건 위반입니다.") from None


# --- Feedback comments (nested under feedback) ---


@router.get(
    "/feedbacks/{feedback_id}/comments",
    response_model=list[FeedbackCommentResponse],
)
async def forma_list_feedback_comments(
    feedback_id: int,
    db: AsyncSession = Depends(get_db),
):
    rows = await FeedbackCommentController(db).list_by_feedback(feedback_id)
    return [FeedbackCommentResponse.model_validate(r) for r in rows]


@router.post(
    "/feedbacks/{feedback_id}/comments",
    response_model=FeedbackCommentResponse,
)
async def forma_create_feedback_comment(
    feedback_id: int,
    req: FeedbackCommentNestedCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await FeedbackCommentController(db).create_for_feedback(
            feedback_id, req
        )
        return FeedbackCommentResponse.model_validate(row)
    except ValueError as e:
        raise _not_found(str(e)) from e
    except IntegrityError:
        await db.rollback()
        raise _integrity("제약 조건 위반입니다.") from None


# --- Video ↔ practice match ---


@router.post(
    "/videos/{video_id}/practice-matches",
    response_model=VideoPracticeMatchResponse,
)
async def forma_create_video_practice_match(
    video_id: int,
    req: VideoPracticeMatchNestedCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await VideoPracticeMatchController(db).create_for_video(video_id, req)
        return VideoPracticeMatchResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 video/practice id가 없거나 제약 조건 위반입니다.") from None


# --- User skills ---


@router.get("/users/{user_id}/skills", response_model=list[UserSkillResponse])
async def forma_list_user_skills(user_id: int, db: AsyncSession = Depends(get_db)):
    rows = await UserSkillController(db).list_by_user(user_id)
    return [UserSkillResponse.model_validate(r) for r in rows]


@router.post("/users/{user_id}/skills", response_model=UserSkillResponse)
async def forma_create_user_skill(
    user_id: int,
    req: UserSkillNestedCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await UserSkillController(db).create_for_user(user_id, req)
        return UserSkillResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 user/practice id가 없거나 제약 조건 위반입니다.") from None


# --- Subscription plans (master) ---


@router.get("/subscription-plans", response_model=list[SubscriptionPlanResponse])
async def forma_list_subscription_plans(db: AsyncSession = Depends(get_db)):
    rows = await SubscriptionPlansController(db).list_plans()
    return [SubscriptionPlanResponse.model_validate(r) for r in rows]


@router.post("/subscription-plans", response_model=SubscriptionPlanResponse)
async def forma_create_subscription_plan(
    req: SubscriptionPlanCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await SubscriptionPlansController(db).create_plan(req)
        return SubscriptionPlanResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("중복된 plan_code이거나 제약 조건 위반입니다.") from None


# --- Subscriptions & payments ---


@router.get("/users/{user_id}/subscription", response_model=SubscriptionResponse)
async def forma_get_user_subscription(
    user_id: int, db: AsyncSession = Depends(get_db)
):
    row = await SubscriptionsController(db).get_active_for_user(user_id)
    if row is None:
        raise _not_found("활성 구독이 없습니다.")
    return SubscriptionResponse.model_validate(row)


@router.post("/users/{user_id}/subscription", response_model=SubscriptionResponse)
async def forma_create_user_subscription(
    user_id: int,
    req: SubscriptionNestedCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await SubscriptionsController(db).create_for_user(user_id, req)
        return SubscriptionResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 user id가 없거나 제약 조건 위반입니다.") from None


@router.post(
    "/subscriptions/{subscription_id}/payment-logs",
    response_model=PaymentLogResponse,
)
async def forma_create_payment_log(
    subscription_id: int,
    req: PaymentLogNestedCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await PaymentLogController(db).create_for_subscription(
            subscription_id, req
        )
        return PaymentLogResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 subscription/user id가 없거나 제약 조건 위반입니다.") from None


# --- Ads ---


@router.get("/ads", response_model=list[AdResponse])
async def forma_list_ads(db: AsyncSession = Depends(get_db)):
    rows = await AdsController(db).list_ads()
    return [AdResponse.model_validate(r) for r in rows]


@router.post("/ads", response_model=AdResponse)
async def forma_create_ad(req: AdCreateRequest, db: AsyncSession = Depends(get_db)):
    try:
        row = await AdsController(db).create_ad(req)
        return AdResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity() from None


@router.post("/users/{user_id}/ad-contracts", response_model=UsersAdResponse)
async def forma_create_users_ad(
    user_id: int,
    req: UsersAdNestedCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await UsersAdController(db).create_contract(user_id, req)
        return UsersAdResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 user/ad id가 없거나 제약 조건 위반입니다.") from None


@router.post(
    "/videos/{video_id}/ad-exposures",
    response_model=AdLinkResponse,
)
async def forma_record_ad_exposure(
    video_id: int,
    req: AdExposureCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await AdLinkController(db).record_exposure(video_id, req)
        return AdLinkResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 video/ad id가 없거나 제약 조건 위반입니다.") from None


@router.get(
    "/ads/{ad_id}/stats/daily",
    response_model=list[AdStatsDailyResponse],
)
async def forma_list_ad_stats_daily(
    ad_id: int,
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
    db: AsyncSession = Depends(get_db),
):
    rows = await AdStatsDailyController(db).list_for_ad(ad_id, from_date, to_date)
    return [AdStatsDailyResponse.model_validate(r) for r in rows]


@router.post(
    "/ads/{ad_id}/stats/daily",
    response_model=AdStatsDailyResponse,
)
async def forma_create_ad_stats_daily(
    ad_id: int,
    req: AdStatsDailyNestedCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        row = await AdStatsDailyController(db).create_for_ad(ad_id, req)
        return AdStatsDailyResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise _integrity("참조 ad id가 없거나 제약 조건 위반입니다.") from None
