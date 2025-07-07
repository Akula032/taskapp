from fastapi import APIRouter, HTTPException

# from httpx import patch
from peewee import IntegrityError
from typing import List


from modules.staff.schema import (
    StaffCreateSchema,
    StaffResponseSchema,
    StaffUpdateSchema,
)
from modules.staff.service import StaffService

router = APIRouter()


@router.post(  # staff登録
    "/staffs",
    response_model=StaffResponseSchema,
    status_code=201,
)  # prefixはmain.pyで指定するのでここでは/staffsとする
def create_staff(staff_data: StaffCreateSchema):
    try:
        new_staff = StaffService.create_new_staff(staff_data)
        return new_staff
    except IntegrityError:
        # サービス層から送出されたIntegrityErrorをここでとる
        raise HTTPException(
            status_code=409,
            detail=f"職員ID '{staff_data.code}' は既に使用されています。",
        )
    except Exception as e:
        # その他の予期せぬエラー
        raise HTTPException(status_code=500, detail=f"エラーが発生しました: {e}")


@router.get(  # staff取得　active=Trueの条件付き　リストで取得
    "/staffs", response_model=List[StaffResponseSchema], tags=["Staffs"]
)
def get_staff_list():
    try:
        staff_list = StaffService.get_all_staff()
        return staff_list
    except Exception as e:
        # データベース接続エラーなどが起きた場合
        raise HTTPException(status_code=500, detail=f"エラーが発生しました: {e}")


@router.get(  # id指定でstaff取得
    "/staffs/{staff_id}", response_model=StaffResponseSchema, tags=["Staffs"]
)
def get_staff_detail(staff_id: int):
    staff = StaffService.get_staff_by_id(staff_id)
    # サービスからNoneが帰ってきたばあいまたはactiveがFalse
    if staff is None:
        raise HTTPException(status_code=404, detail="指定した職員が見つかりません。")

    return staff


@router.patch(  # id指定で編集
    "/staffs/{staff_id}", response_model=StaffResponseSchema, tags=["Staffs"]
)
def update_staff(staff_id: int, staff_data: StaffUpdateSchema):
    try:
        updated_staff = StaffService.update_staff_by_id(staff_id, staff_data)
        if updated_staff is None:  # サービスからのNoneはここに来る
            raise HTTPException(
                status_code=404, detail="更新対象の職員が見つかりません。"
            )
        return updated_staff
    except IntegrityError:  # 重複エラー
        raise HTTPException(status_code=409, detail="職員IDは既に使用されています。")
        # サービスstaff.save()のときIntegrityErrorがでたときexceptでとる
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500, detail=f"エラーが発生しました: {e}"
    #     ) #サーバーエラーとか


@router.patch(  # id指定で非アクティブ化
    "/staffs/{staff_id}/deactivate", response_model=StaffResponseSchema, tags=["Staffs"]
)
def deactivate_staff(staff_id: int):
    deactivated_staff = StaffService.deactivate_staff_by_id(staff_id)

    if deactivated_staff is None:
        raise HTTPException(status_code=404, detail="対象の職員が見つかりません。")

    return deactivated_staff
