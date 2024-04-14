import requests

cookies = {
    '_ga': 'GA1.1.720805129.1711821463',
    '_gcl_au': '1.1.803809556.1711821470',
    '_hjSessionUser_3724640': 'eyJpZCI6IjBkNjE4YzBlLWQ4YzAtNWZjYy1iZjgwLTNhNjcyYjk5NDkyZCIsImNyZWF0ZWQiOjE3MTE4MjE0NzY1MDAsImV4aXN0aW5nIjp0cnVlfQ==',
    'PHPSESSID': '9asud5uo7e3gn4c8lra1d6t2c3',
    '_hjSession_3724640': 'eyJpZCI6IjQ2NjlkYWE4LTNjMGUtNDBjZi04ODdkLTkzNWMzYTE3YzJhOSIsImMiOjE3MTMwMDAxMjc1NDUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
    '_ga_EN8BN980LH': 'GS1.1.1712999874.17.1.1713000989.17.0.0',
    '_ga_FMK4KRGVF2': 'GS1.1.1713000120.17.1.1713000990.0.0.0',
    '_ga_94GCJ4Q0CE': 'GS1.1.1713000120.17.1.1713000990.0.0.0',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': '_ga=GA1.1.720805129.1711821463; _gcl_au=1.1.803809556.1711821470; _hjSessionUser_3724640=eyJpZCI6IjBkNjE4YzBlLWQ4YzAtNWZjYy1iZjgwLTNhNjcyYjk5NDkyZCIsImNyZWF0ZWQiOjE3MTE4MjE0NzY1MDAsImV4aXN0aW5nIjp0cnVlfQ==; PHPSESSID=9asud5uo7e3gn4c8lra1d6t2c3; _hjSession_3724640=eyJpZCI6IjQ2NjlkYWE4LTNjMGUtNDBjZi04ODdkLTkzNWMzYTE3YzJhOSIsImMiOjE3MTMwMDAxMjc1NDUsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; _ga_EN8BN980LH=GS1.1.1712999874.17.1.1713000989.17.0.0; _ga_FMK4KRGVF2=GS1.1.1713000120.17.1.1713000990.0.0.0; _ga_94GCJ4Q0CE=GS1.1.1713000120.17.1.1713000990.0.0.0',
    'Origin': 'https://dentalia.com',
    'Referer': 'https://dentalia.com/clinica/?jsf=jet-engine:clinicas-archive&tax=estados:16',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'jsf': 'jet-engine:clinicas-archive',
    'tax': 'estados:16',
    'nocache': '1713000988',
}

data = {
    'action': 'jet_engine_ajax',
    'handler': 'get_listing',
    'page_settings[post_id]': '5883',
    'page_settings[queried_id]': '344706|WP_Post',
    'page_settings[element_id]': 'c1b6043',
    'page_settings[page]': '1',
    'listing_type': 'elementor',
    'isEditMode': 'false',
}
