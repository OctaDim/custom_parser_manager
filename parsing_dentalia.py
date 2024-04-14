from managers_custom.parser_manager_custom import ParserManager
import requests
from bs4 import BeautifulSoup

from utils_custom.utils import (compose_full_filename,
                                create_fake_headers,
                                create_json_file,
                                create_dir_if_not_exists,
                                read_json_file,
                                make_slashed_name,
                                create_csv_file,
                                )

from dentalia.fetch_requests import all_clinics_request_params
from dentalia.fetch_requests import admin_ajax_request_params

# ##### GETTING MAIN PAGE HTML FILE AND AREAS ##########################
url = "https://dentalia.com/"

local_html_full_filename = compose_full_filename(
    directories_paths=("dentalia", "html_pages"),
    file_name="local_dentalia.html")

with ParserManager(url, headers=create_fake_headers(),
                   local_full_filename=local_html_full_filename,
                   file_rewrite=False) as parsed_main_page:

    all_regions = parsed_main_page.find("div", class_="jet-listing-grid__items grid-col-desk-1 grid-col-tablet-1 grid-col-mobile-1 jet-listing-grid--231")

    all_clinics_by_region_dict = {}
    all_clinics_dicts_list = []

    for region in all_regions:
        region_name = region.find(
            "div", class_="jet-listing-dynamic-field__content").string.strip()

        region_link = region.find("h2").find("a").get("href").strip()
        region_id = region.get("data-post-id")


        # url = (f"https://dentalia.com/clinica/"
        #        f"?jsf=jet-engine:clinicas-archive&tax=estados:{region_id}")
        # requests.get(url=url)


        url = "https://dentalia.com/wp-admin/admin-ajax.php"
        cookies = admin_ajax_request_params.cookies
        headers = admin_ajax_request_params.headers
        data = admin_ajax_request_params.data
        admin_ajax_request_params.data["query[_tax_query_estados]"] = f"{region_id}"
        response = requests.post(url=url, cookies=cookies, headers=headers, data=data)

        geo_locations_dicts_list_from_ajax = response.json().get("markers")
        clinics_geo_dict = {}

        for clinic_geo_dict_from_ajax in geo_locations_dicts_list_from_ajax:
            clinic_id = clinic_geo_dict_from_ajax.get("id")
            geo_lat = clinic_geo_dict_from_ajax.get("latLang").get("lat")
            geo_lng = clinic_geo_dict_from_ajax.get("latLang").get("lng")

            clinics_geo_dict[str(clinic_id)] = [geo_lat, geo_lng]


        url = "https://dentalia.com/clinica/"
        params = all_clinics_request_params.params
        cookies = all_clinics_request_params.cookies
        headers = all_clinics_request_params.headers
        data = all_clinics_request_params.data
        all_clinics_request_params.params["tax"] = f"estados:{region_id}"

        response = requests.post(url=url, params=params, cookies=cookies,
                                 headers=headers, data=data)

        html_content = response.json().get("data").get("html")
        clinics_parsed_source = BeautifulSoup(html_content, "lxml")

        all_clinics = clinics_parsed_source.find("div", class_="jet-listing-grid__items")
        all_clinics = all_clinics.find_all("div", class_="jet-listing-grid__item")

        clinics_dict = {}

        for clinic in all_clinics:
            clinic_id = clinic.get("data-post-id")

            clinic_name = clinic.find(
                "h3",
                class_="elementor-heading-title elementor-size-default").text.strip()

            clinic_info = clinic.find_all("div", class_="jet-listing-dynamic-field__content")
            clinic_address = clinic_info[0].text.strip()

            clinic_geo = clinics_geo_dict.get(clinic_id)

            clinic_phone = clinic_info[1].text.strip()
            clinic_phone = clinic_phone.replace("Teléfono(s): ", "")
            clinic_phone_list = clinic_phone.split("\r\n")
            clinic_phone_list = [ph.strip() for ph in clinic_phone_list]

            clinic_worktime = clinic_info[2].text.strip()
            clinic_worktime = clinic_worktime.replace("Horario: ", "")
            clinic_worktime_list = clinic_worktime.split("\r\n")
            clinic_worktime_list = [wt.strip() for wt in clinic_worktime_list]

            all_clinics_dicts_list.append({"clinic_id": clinic_id,
                                           "clinic_name": clinic_name,
                                           "clinic_address": clinic_address,
                                           "clinic_geo": clinic_geo,
                                           "clinic_phone": clinic_phone_list,
                                           "clinic_worktime": clinic_worktime_list
                                           })

            clinics_dict[clinic_name] = {"clinic_id": clinic_id,
                                         "clinic_name": clinic_name,
                                         "clinic_address": clinic_address,
                                         "clinic_geo": clinic_geo,
                                         "clinic_phone": clinic_phone_list,
                                         "clinic_worktime": clinic_worktime_list}

            print(f"\tParsed:  Region: {region_name} | Clinic: {clinic_name}")

        all_clinics_by_region_dict[region_name] = clinics_dict

    json_full_filename = compose_full_filename(
        directories_paths=("dentalia", "json_files"),
        file_name="all_clinics_dicts_list.json")

    create_json_file(json_full_filename=json_full_filename,
                     data_dictionary=all_clinics_dicts_list,
                     file_rewrite=True)


    json_full_filename = compose_full_filename(
        directories_paths=("dentalia", "json_files"),
        file_name="all_clinics_by_region.json")

    create_json_file(json_full_filename=json_full_filename,
                     data_dictionary=all_clinics_by_region_dict,
                     file_rewrite=True)
