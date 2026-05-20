from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db

from .controllers.ad_link_controller import AdLinkController
from .controllers.forma_seed_controller import FormaSeedController
from .controllers.ads_controller import AdsController
from .controllers.feedback_controller import FeedbackController
from .controllers.frame_controller import FrameController
from .controllers.practice_controller import PracticeController
from .controllers.sports_controller import SportsController
from .controllers.subscriptions_controller import SubscriptionsController
from .controllers.users_controller import UsersController
from .controllers.video_controller import VideoController
from .schemas.ad_link_schema import AdLinkCreateRequest, AdLinkResponse
from .schemas.ads_schema import AdCreateRequest, AdResponse
from .schemas.feedback_schema import FeedbackCreateRequest, FeedbackResponse
from .schemas.frame_schema import FrameCreateRequest, FrameResponse
from .schemas.practice_schema import PracticeCreateRequest, PracticeResponse
from .schemas.sports_schema import SportCreateRequest, SportResponse
from .schemas.subscriptions_schema import SubscriptionCreateRequest, SubscriptionResponse
from .schemas.seed_schema import SeedDemoCsvResponse
from .schemas.users_schema import FormaUserCreateRequest, FormaUserResponse
from .schemas.video_schema import VideoCreateRequest, VideoResponse

router = APIRouter(prefix="/forma", tags=["forma"])


@router.post("/seed-demo-csv", response_model=SeedDemoCsvResponse)
async def forma_seed_demo_csv(
    limit: int = 15,
    db: AsyncSession = Depends(get_db),
):
    """공개 도메인 국가 목록 CSV로 데모 user/video/sport/ad/ad_link 행을 Neon( Postgres)에 적재합니다."""
    try:
        return await FormaSeedController(db).seed_demo_from_country_csv(limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/users", response_model=FormaUserResponse)
async def forma_create_user(
    req: FormaUserCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        user = await UsersController(db).create_user(req)
        return FormaUserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


@router.get("/users", response_model=list[FormaUserResponse])
async def forma_list_users(db: AsyncSession = Depends(get_db)):
    users = await UsersController(db).list_users()
    return [FormaUserResponse.model_validate(u) for u in users]


@router.post("/sports", response_model=SportResponse)
async def forma_create_sport(
    req: SportCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await SportsController(db).create_sport(req)
        return SportResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="중복되었거나 제약 조건 위반입니다.",
        ) from None


@router.get("/sports", response_model=list[SportResponse])
async def forma_list_sports(db: AsyncSession = Depends(get_db)):
    rows = await SportsController(db).list_sports()
    return [SportResponse.model_validate(r) for r in rows]


@router.post("/videos", response_model=VideoResponse)
async def forma_create_video(
    req: VideoCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await VideoController(db).create_video(req)
        return VideoResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="참조 user/sport id가 없거나 제약 조건 위반입니다.",
        ) from None


@router.get("/videos", response_model=list[VideoResponse])
async def forma_list_videos(db: AsyncSession = Depends(get_db)):
    rows = await VideoController(db).list_videos()
    return [VideoResponse.model_validate(r) for r in rows]


@router.post("/frames", response_model=FrameResponse)
async def forma_create_frame(
    req: FrameCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await FrameController(db).create_frame(req)
        return FrameResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="참조 video_id가 없거나 제약 조건 위반입니다.",
        ) from None


@router.get("/frames", response_model=list[FrameResponse])
async def forma_list_frames(db: AsyncSession = Depends(get_db)):
    rows = await FrameController(db).list_frames()
    return [FrameResponse.model_validate(r) for r in rows]


@router.post("/feedbacks", response_model=FeedbackResponse)
async def forma_create_feedback(
    req: FeedbackCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await FeedbackController(db).create_feedback(req)
        return FeedbackResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="참조 video/frame id가 없거나 제약 조건 위반입니다.",
        ) from None


@router.get("/feedbacks", response_model=list[FeedbackResponse])
async def forma_list_feedbacks(db: AsyncSession = Depends(get_db)):
    rows = await FeedbackController(db).list_feedbacks()
    return [FeedbackResponse.model_validate(r) for r in rows]


@router.post("/practices", response_model=PracticeResponse)
async def forma_create_practice(
    req: PracticeCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await PracticeController(db).create_practice(req)
        return PracticeResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="참조 id가 없거나 제약 조건 위반입니다.",
        ) from None


@router.get("/practices", response_model=list[PracticeResponse])
async def forma_list_practices(db: AsyncSession = Depends(get_db)):
    rows = await PracticeController(db).list_practices()
    return [PracticeResponse.model_validate(r) for r in rows]


@router.post("/subscriptions", response_model=SubscriptionResponse)
async def forma_create_subscription(
    req: SubscriptionCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await SubscriptionsController(db).create_subscription(req)
        return SubscriptionResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="참조 user id가 없거나 제약 조건 위반입니다.",
        ) from None


@router.get("/subscriptions", response_model=list[SubscriptionResponse])
async def forma_list_subscriptions(db: AsyncSession = Depends(get_db)):
    rows = await SubscriptionsController(db).list_subscriptions()
    return [SubscriptionResponse.model_validate(r) for r in rows]


@router.post("/ads", response_model=AdResponse)
async def forma_create_ad(req: AdCreateRequest, db: AsyncSession = Depends(get_db)):
    try:
        row = await AdsController(db).create_ad(req)
        return AdResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="참조 user id가 없거나 제약 조건 위반입니다.",
        ) from None


@router.get("/ads", response_model=list[AdResponse])
async def forma_list_ads(db: AsyncSession = Depends(get_db)):
    rows = await AdsController(db).list_ads()
    return [AdResponse.model_validate(r) for r in rows]


@router.post("/ad-links", response_model=AdLinkResponse)
async def forma_create_ad_link(
    req: AdLinkCreateRequest, db: AsyncSession = Depends(get_db)
):
    try:
        row = await AdLinkController(db).create_ad_link(req)
        return AdLinkResponse.model_validate(row)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="참조 video/ad id가 없거나 제약 조건 위반입니다.",
        ) from None


@router.get("/ad-links", response_model=list[AdLinkResponse])
async def forma_list_ad_links(db: AsyncSession = Depends(get_db)):
    rows = await AdLinkController(db).list_ad_links()
    return [AdLinkResponse.model_validate(r) for r in rows]
