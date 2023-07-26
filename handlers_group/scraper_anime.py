from parsel import Selector
import requests
from random import choice, randint
from bs4 import BeautifulSoup

def recommend(status=None, season=None):
    xpath_anime = '//a[@class="cover anime-tooltip"]/@href'
    xpath_max_page = '//span[@class="link-total"]/text()'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    serch_tree = lambda t, x: t.xpath(x).getall()

    link_status = f'/status/{status}' if status else ""
    link_season = f'/season/{season}' if season else ""
    link_score = f'/score/7' if status != 'anons' else ""

    link = f"https://shikimori.me/animes/kind/tv{link_status}{link_season}{link_score}"

    requests_max_pages = requests.get(link, headers=headers).text
    selector_num_max_page = Selector(text=requests_max_pages)
    num_max_page = int(serch_tree(selector_num_max_page, xpath_max_page)[0])
    rand_page = randint(0, num_max_page)

    search = link + f"/page/{rand_page}"
    requests_recommended_anime_list = requests.get(search, headers=headers).text
    trees = Selector(text=requests_recommended_anime_list)
    recommend_anime_link = choice(serch_tree(trees, xpath_anime))
    return recommend_anime_link


def recommend_print(link):
    xpath_title = '//h1/text()'
    xpath_rating = '//div[contains(concat(" ", @class, " "), "score-value")]/text()'
    xpath_date = '//div[@class="line"][div[@class="key" and contains(text(), "Статус:")]]/div[@class="value"]/text()'
    xpath_date_released = '//div[@class="line"][div[@class="key" and contains(text(), "Статус:")]]/div[@class="value"]/span[2]/text()'
    xpath_genres = '//span[@class="genre-ru"]/text()'
    xpath_episodes = '//div[@class="line"][div[@class="key" and contains(text(), "Эпизоды:")]]/div[@class="value"]/text()'
    xpath_description = '//div[@class="b-text_with_paragraphs"]'
    xpath_image = '//picture/img/@srcset'
    xpath_released = '//span[@class="b-anime_status_tag released"]'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }

    requests_recommend_anime = requests.get(link, headers=headers).text
    tree = Selector(text=requests_recommend_anime)

    serch_tree = lambda t, x: t.xpath(x).getall()

    # аниме
    recommend_anime = {}

    # название аниме
    title = serch_tree(tree, xpath_title)
    recommend_anime['title'] = '/'.join(title)

    # рейтинг аниме
    tree_rating = serch_tree(tree, xpath_rating)
    rating = tree_rating if tree_rating else ['0']
    recommend_anime['rating'] = f'*Рейтинг: *' + rating[0]

    # дата релиза
    if not serch_tree(tree, xpath_released):
        recommend_anime['date_release'] = '*Релиз:*' + serch_tree(tree, xpath_date)[0]
    else:
        recommend_anime['date_release'] = '*Релиз: *' + serch_tree(tree, xpath_date_released)[0]

    # эпизоды аниме
    episodes = serch_tree(tree, xpath_episodes)[0] if serch_tree(tree, xpath_episodes) else '?'
    recommend_anime['episodes'] = '*Эпизоды: *' + episodes

    # жанры аниме
    recommend_anime['genres'] = "*Жанры:* " + ", ".join(serch_tree(tree, xpath_genres))

    # описание аниме
    description_html = serch_tree(tree, xpath_description)
    recommend_anime['description'] = 'Нет описания'
    if description_html:
        recommend_anime['description'] = BeautifulSoup(description_html[0], 'html.parser').get_text()

    # картинка аниме
    recommend_anime['image'] = serch_tree(tree, xpath_image)[0][:-3]

    # ссылка
    recommend_anime['link'] = link[28:]
    return recommend_anime