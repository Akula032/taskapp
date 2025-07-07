from peewee import IntegrityError
from typing import List, Optional

from modules.staff.model import Staff
from modules.staff.schema import StaffCreateSchema, StaffUpdateSchema


class StaffService:
    @staticmethod  # 関数定義のおまじない
    def create_new_staff(staff_data: StaffCreateSchema) -> Staff:  # スタッフ追加
        try:
            new_staff = Staff.create(code=staff_data.code, name=staff_data.name)
            return new_staff
        except IntegrityError as e:
            # エラーはAPI層で処理予定、ここではそのまま送出する
            raise e
        # 新しいスタッフのデータを受け取り、データベースに保存する
        # 成功した場合は、作成されたStaffオブジェクトを返す
        # codeの制約違反の場合は、IntegrityErrorをそのまま送出する

    @staticmethod  # Get
    def get_all_staff() -> List[Staff]:  # スタッフGet
        return list(Staff.select().where(Staff.active).order_by(Staff.id))
        # スタッフを全て取得。active=Trueの条件付き
        # (Staff.active == True)はやめた

    @staticmethod  # id指定Get
    def get_staff_by_id(staff_id: int) -> Optional[Staff]:  # idでGet
        return Staff.get_or_none((Staff.id == staff_id) & (Staff.active))
        # 単一のスタッフをIDで取得する
        # active=Trueのスタッフのみを対象とする
        # 見つからない場合はNoneを返す

    @staticmethod  # id指定して編集
    def update_staff_by_id(
        staff_id: int, staff_data: StaffUpdateSchema
    ) -> Optional[Staff]:
        # idで対象を探す
        staff = Staff.get_or_none((Staff.id == staff_id) & (Staff.active))
        # なかったらAPIにNoneを返す
        if staff is None:
            return None
        # staff_dataには入力されたデータ
        update_data = staff_data.model_dump(exclude_unset=True)  # Pydanticのメゾット
        for key, value in update_data.items():
            setattr(staff, key, value)
            # 受け取ったstaff,keyを使って更新
        try:
            staff.save()
            return staff
        except IntegrityError as e:
            # codeの重複エラーDBで設定したユニークを検知
            raise e

    @staticmethod  # 削除（非アクティブ化）
    def deactivate_staff_by_id(staff_id: int) -> Optional[Staff]:
        staff = Staff.get_or_none((Staff.id == staff_id) & (Staff.active))

        # スタッフが見つからなければ、Noneを返す
        if staff is None:
            return None
        # 指定されたものが見つかれば、Falseにして保存
        staff.active = False
        staff.save()
        return staff
