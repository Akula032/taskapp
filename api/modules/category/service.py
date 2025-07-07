from .model import Category as CategoryModel


def get_all_categories() -> list[CategoryModel]:  # アクティブなカテゴリを全て取得
    return list(CategoryModel.select().where(CategoryModel.active))


# def create_category(category_data: CategoryCreate) -> CategoryModel: # 新規作成ロジックもここに

#     return CategoryModel.create(**category_data.model_dump())
