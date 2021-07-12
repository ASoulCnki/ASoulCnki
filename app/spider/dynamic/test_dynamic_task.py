import get_dynamic_base_data
import get_dynamic_full_data


def crawl_a_member(mid):
    get_dynamic_base_data.create_requests_and_save_data(mid)


if __name__ == '__main__':
    asoul_member_ids = [672346917, 672342685, 672353429, 351609538, 672328094, 703007996]
    get_dynamic_full_data.task(asoul_member_ids)
