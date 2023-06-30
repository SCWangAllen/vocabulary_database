from django.db import models
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re
from notion_client import Client
import requests
import os
import random
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except ValueError:
        return False


vocabulary_token = os.getenv("NOTION_KEY")
notion = Client(auth=vocabulary_token)
icons = ["📚", "💼", "🌐", "💡", "🚀", "📝", "🧠", "📆", "⏰", "🎓"]
# Create your models here.
# def crawler_the_cambridge():


class Word(models.Model):
    english_word = models.CharField(max_length=200)
    chinese_word = models.CharField(max_length=200)


def get_word_info(word) -> dict:
    """_summary_
        This is a function to get the word's definition, translation and examples from cambridge dictionary, and return a dict.
        Use selenium to get the data we need .
    Args:
        word (_type_): _description_

    Returns:
        dict: _description_
    """
    word=word.lower()
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    url = 'https://dictionary.cambridge.org/zht/'
    driver.get(url)

    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(word)
    search_box.submit()

    wait = WebDriverWait(driver, 2)
    # 裡外處理例外
    try:
        element = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'def-block.ddef_block')))
    except:
        driver.quit()
        return {'definition': '無此單字', 'translation': '無此單字', 'examples': []}
    word_element = driver.find_element(By.CSS_SELECTOR, '.headword.dhw.dpos-h_hw').text
    def_blocks = driver.find_elements(By.CSS_SELECTOR, '.def-block.ddef_block')
    # 因為他是一塊一塊的，所以要用for迴圈把他們一個一個抓出來
    definitions = []

    for i, block in enumerate(def_blocks):
        # 提取英文定義
        def_text = block.find_element(By.CSS_SELECTOR, '.def.ddef_d.db').text

        # 提取中文翻譯
        trans_text = block.find_element(
            By.CSS_SELECTOR, '.trans.dtrans.dtrans-se.break-cj').text

        # 提取英文例句
        eng_examples = block.find_elements(
            By.CSS_SELECTOR, '.examp.dexamp .eg.deg')

        # 提取中文例句
        chi_examples = block.find_elements(
            By.CSS_SELECTOR, '.examp.dexamp .trans.dtrans.dtrans-se.hdb.break-cj')

        # 使用zip函數將英文例句和中文例句配對起來
        examples = [(eng.text, chi.text)
                    for eng, chi in zip(eng_examples, chi_examples)]

        definitions.append({
            'definition': def_text,
            'translation': trans_text,
            'examples': examples,
        })

    driver.quit()
    print(word_element)
    return {'definition':definitions,'word':word_element}



# 這是新增page的函數

def insert_to_notion(word_info, title: str = '', tag: str = "work",url: str='http://example.com') -> dict:  
    blocks = []

    for definition in word_info:
        definition_block = {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Definition:", "link": None}
                    }
                ],
                "color":"blue_background",
            }
        }
        blocks.append(definition_block)

        definition_text = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": definition['definition'], "link": None}
                    }
                ],
            }
        }
        blocks.append(definition_text)

        translation_block = {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "Translation:", "link": None}
                    }
                ],
                "color":"green_background",
            }
        }
        blocks.append(translation_block)

        translation_text = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": definition['translation'], "link": None}
                    }
                ],
            }
        }
        blocks.append(translation_text)

        for i, example in enumerate(definition['examples']):
            example_block = {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": f"Example {i+1}:", "link": None}
                        }
                    ],
                    "color":"purple_background",
                    
                },
                
                 
            }
            blocks.append(example_block)

            english_example_text = {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": f"English: {example[0]}", "link": None}
                        }
                    ],
                }
            }
            blocks.append(english_example_text)

            chinese_example_text = {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": f"Chinese: {example[1]}", "link": None}
                        }
                    ],
                }
            }
            blocks.append(chinese_example_text)
    if len(blocks)>100:
        blocks=blocks[:100]
    if is_valid_url(url):
        url_for_link=url
    else:
        url_for_link='http://example.com'
    page = notion.pages.create(
        parent={"database_id": '9ed5b492835e40eb93cc72d38edc3fc7'},
        properties={
            "keyword": {"title": [{"type": "text", "text": {"content": title}}]},
            "tag": {"type": "multi_select", "multi_select": [{"name": tag}]},
             "url": {"rich_text": [{"type": "text", "text": 
                                    {"content": url,
                                     'link':{'url':url_for_link}
                                     }
                                    }]},
            "meaning": {"rich_text": [{"type": "text", "text": {"content": word_info[0]['translation']}}]}

        },
        children=blocks,
        icon={"type": "emoji", "emoji": "📚"}
    )

    return page
# 這是filter的函數
def filter_pages_by_keyword(keyword: str):
    # 创建一个过滤条件，根据"keyword"属性的值进行过滤
    filter_condition = {
    "and": [
        {
            "property": "keyword",
            "title": {
                "equals": keyword
            }
        },
    ]
}

    # 使用过滤条件来查询数据库
    response = notion.databases.query(
        database_id='9ed5b492835e40eb93cc72d38edc3fc7',
        filter=filter_condition
    )

    # 返回查询结果
    return response

def add_url_to_page(page_id: str, new_url: str):
    # 取得filter過後頁面的資料
    page = notion.pages.retrieve(page_id=page_id)

    # 取得這個page url的相關資料
    current_url_content = page['properties']['url']['rich_text']

    # 在原本的content後面加上
    new_url_content = current_url_content + [{
        "type": "text",
        "text": {
            "content": "  ,  " ,
        }
    }]
    if is_valid_url(new_url):
        new_url_for_link=new_url
    else:
        new_url_for_link='http://example.com'
    new_url_content = new_url_content + [{
        "type": "text",
        "text": {
            "content":  new_url,
            "link": {
                "url": new_url_for_link
            }
        }
    }]


    # 更新页面的 "url" 属性
    updated_page = notion.pages.update(
        page_id=page_id,
        properties={
            "url": {
                "rich_text": new_url_content
            }
        }
    )

    return updated_page

def filter_or_insert(keyword: str, word_info, title: str = '', tag: str = "TBD", url: str='http://example.com'):
    # 首先，尝试根据关键词查找页面
    response = filter_pages_by_keyword(keyword)

    # 如果找不到任何页面，那么插入一个新的页面
    if not response['results']:
        insert_to_notion(word_info, title, tag, url)
        return {"message": "Insertion successful", "success": True}

    # 如果找到了页面，那么更新这些页面的 URL
    for page in response['results']:
        add_url_to_page(page['id'], url)

    return {"message": "Page(s) updated", "success": True}


