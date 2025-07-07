from modules.status.model import Status as StatusModel


def get_all_statuses() -> list[StatusModel]:
    return list(StatusModel.select().where(StatusModel.active))
