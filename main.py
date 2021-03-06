from urllib.request import urlopen
import re
import csv


def get_url_contents(url):
    return urlopen(url).read()


def get_substrings_between_tags(content, source, first_tag, second_tag):
    result_list = list(filter(lambda x: source.lower() not in x.lower(),
                              re.findall(first_tag + "(.+)" + second_tag, content)))

    result_list_mapped = list(map(lambda x: x.replace(',', ''), result_list))

    return list(zip(result_list_mapped, [source for _ in range(0, len(result_list))]))


def write_to_csv(data):
    output_file = open("output.csv", "w")
    output_writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    output_writer.writerow(['Title', 'Source'])

    for record in data:
        output_writer.writerow(record)


def write_to_csv_complete_table(data):
    nodes = dict()
    id = 1
    for item in data:
        nodes[item[0]] = id
        id = id + 1

    source_url_id = set([x[1] for x in data])

    for item in source_url_id:
        nodes[item] = id
        id = id + 1

    complete_data = list()

    for item in data:
        complete_data.append((nodes[item[0]], item[0], nodes[item[0]], nodes[item[1]]))

    for item in source_url_id:
        complete_data.append((nodes[item], item, nodes[item], nodes[item]))

    output_file = open("output_complete.csv", "w")
    output_writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    output_writer.writerow(['Id', 'Label', "Source", 'Target'])

    for record in complete_data:
        output_writer.writerow(record)


def scrape_urls():
    url_records = open("/Users/georgehuzum/PycharmProjects/ARMS/urls.txt").read().split('\n')
    result_list = list()

    for i in range(0, len(url_records), 2):
        source_url = url_records[i]
        url = url_records[i + 1]

        url_content_to_parse = get_url_contents(url).decode('UTF-8')
        result_list = result_list + get_substrings_between_tags(url_content_to_parse, source_url, "<title>", "</title>")

    write_to_csv(result_list)
    write_to_csv_complete_table(result_list)


scrape_urls()
