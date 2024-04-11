from managers_custom.parser_manager_custom import  ParserManager

from utils_custom.utils import (compose_full_filename,
                                create_dir_if_not_exists,
                                create_fake_headers,
                                create_json_file,
                                read_json_file,
                                make_slashed_name,
                                create_csv_file,
                                )


# ##### GETTING MAIN PAGE FILE AND CATEGORIES ##########################
url = "http://www.health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
base_url = "http://www.health-diet.ru"

local_html_full_filename = compose_full_filename(
    directories_paths=("health_diet","html_pages"),
    file_name="local_health_diet.html")

with ParserManager(url, headers=create_fake_headers(),
                   local_full_filename=local_html_full_filename,
                   file_rewrite=False) as parsed_source:

    all_categories= parsed_source.find_all(
        "a", class_="mzr-tc-group-item-href")

    all_categories_dict = {}

    for category in all_categories:
        category_name = category.string.strip()
        category_url = base_url + category.get("href").strip()
        all_categories_dict[category_name] = category_url

    json_full_filename = compose_full_filename(
        directories_paths=("health_diet", "json_files"),
        file_name="all_categories_health_diet.json")

    create_json_file(json_full_filename, all_categories_dict,
                     file_rewrite=False)

# ##### GETTING EACH CATEGORY INFO #####################################
all_categories = read_json_file(json_full_filename)
category_number = 1

products_info_dicts_list_for_csv = []
products_info_dicts_dict_for_json = {}

for category_name, category_url in all_categories.items():

    slashed_name = make_slashed_name(category_name)
    slashed_file_name = (f"{category_number :03d}_"
                         f"{slashed_name}.html")

    local_html_full_filename = compose_full_filename(
        directories_paths=("health_diet", "html_pages", "categories_pages"),
        file_name=slashed_file_name)

    with ParserManager(url=category_url,
                        headers=create_fake_headers(),
                        local_full_filename=local_html_full_filename,
                        file_rewrite=False,
                        not_200_create_local_file=True) as parsed_source:

        table = parsed_source.find("table", class_="mzr-tc-group-table")
        if not table:
            continue

        category_products_tr_list = table.find("tbody").find_all("tr")

        for product_tr in category_products_tr_list:
            product_td_list = product_tr.find_all("td")

            # ############## CREATING DICTS LIST FOR CSV ###############
            product_info_dict_for_csv = {
                "category_name": category_name,
                "product_name": product_td_list[0].find_next().text.strip(),
                "calories": product_td_list[1].text.strip(),
                "proteins": product_td_list[2].text.strip(),
                "fats": product_td_list[3].text.strip(),
                "carbohydrates": product_td_list[4].text.strip()}
            products_info_dicts_list_for_csv.append(product_info_dict_for_csv)

            # ############## CREATING DICTS DICT FOR JSON ##############
            product_info_dict_for_csv = {
                "product_name": product_td_list[0].find_next().text.strip(),
                "calories": product_td_list[1].text.strip(),
                "proteins": product_td_list[2].text.strip(),
                "fats": product_td_list[3].text.strip(),
                "carbohydrates": product_td_list[4].text.strip()}
            products_info_dicts_dict_for_json[category_name]=product_info_dict_for_csv

    category_number += 1

# ######################## CREATING RESULT CSV FILE ####################
csv_full_filename = compose_full_filename(
    ("health_diet", "csv_files"),
    "products_info_with_categories.csv")

csv_headers = ["category_name",
               "product_name",
               "calories",
               "proteins",
               "fats",
               "carbohydrates"]

create_csv_file(csv_full_filename,
                csv_headers=csv_headers,
                data_dicts_list=products_info_dicts_list_for_csv,
                file_rewrite=True)


# ######################## CREATING RESULT JSON FILE ###################
json_full_filename = compose_full_filename(
    ("health_diet","json_files"),
    "products_info_by_categories.json")

create_json_file(json_full_filename,
                 data_dictionary=products_info_dicts_dict_for_json,
                 file_rewrite=True)
