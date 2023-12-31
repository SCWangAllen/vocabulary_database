# Vocabulary Database

## 前言

在學習英語的過程中，Notion 一直是我的得力助手，我習慣在其中記錄自己遇到的新單字並進行筆記。在採納了一些推薦後，我開始使用劍橋英文翻譯網站來查詢陌生的單詞，並將其整理到 Notion 的單詞庫中。經過一段時間的實踐，我們發現這種方法相當繁瑣。首先，需要開啟多個網站；其次，每次都需要手動創建新的頁面，輸入單詞，然後將其整理到 Notion 中。因此，在注意到 Notion 推出其 API 系統的時機，我們決定開發一個能自動化這些繁瑣步驟的專案，用於建立英文筆記的資料庫，當然熟悉過後，也能用來整合自己的其他筆記源。

## 欲解決問題

在開發這個專案的過程中，我們遇到了一些問題需要解決：

1. 如何使用 Notion API?
2. 我們應該通過什麼方式實現這個專案，是 WEB SERVER，還是瀏覽器插件，還是應用程式？
3. 如何設計用於爬取單詞網站的爬蟲（使用網站的 API 太貴）？

## 專案介紹

"vocabulary_database" 是一個使用 Python 和 Django 架構的專案，主要功能如下：

1. 使用 Selenium 網路爬蟲，從劍橋英文翻譯網站自動獲取指定單詞的詳細資訊，包括英文定義、中文翻譯，以及相關的例句。
    
2. 將獲取到的單詞資訊自動儲存到 Notion 頁面中。具體來說，這個功能允許用戶將指定的單詞、其定義、翻譯，以及例句添加到一個 Notion 頁面中。
    
3. 使用 Django 的模型來組織和儲存單詞資訊。具體來說，有一個 "Word" 模型，用於儲存英文單詞和中文單詞。
    


## 安裝

為了運行這個專案，您需要安裝一些必要的 Python 套件，包括：

- Django==4.2.2 # 伺服器
- beautifulsoup4==4.12.2 # 爬蟲
- django-cors-headers==4.1.0 #跨網域請求
- requests==2.31.0 # 爬蟲
- selenium==4.10.0 # 爬蟲
- notion-client==2.0.0 # Notion API整合

您可以透過以下命令來安裝這些套件：

Copy code

`pip install -r requirements.txt`

## 使用方法

待作者更新...

## 專案架構

此專案主要分為兩個部分，一個是 "vocabulary"，另一個是 "cambridge"。

- "vocabulary"：此目錄主要包含 Django 專案的設定檔，如 settings.py、urls.py 等。
    
- "cambridge"：此目錄主要包含與劍橋網站單詞爬取和 Notion 數據儲存相關的代碼，包含 models.py、views.py 等。
    

## 未來規劃

我們將持續改進和擴展此專案，以提供更多的功能和更好的用戶體驗。具體的規劃包括：

1. 優化單詞爬取的效率和準確性。
2. 提供更多的單詞來源，不僅僅是劍橋網站。
3. 針對拼字錯誤的優化
4. 優化 Notion 數據儲存的效率和準確性。

## 結語

透過這個專案，我們希望能讓學習英語的過程更加順暢和高效。如果您有任何問題或建議，歡迎與我們聯繫。感謝您的關注和支持！


#   Vocabulary Database

## Introduction

Throughout my English learning journey, Notion has been my reliable assistant, where I keep track of new vocabulary and take notes. After adopting some recommendations, I started using the Cambridge English Dictionary website to look up unfamiliar words and organize them in my Notion vocabulary database. However, this method proved to be quite cumbersome. Firstly, it involved opening multiple websites. Secondly, I had to manually create new pages, enter the words, and then organize them in Notion. Therefore, when I learned about the release of Notion's API system, I decided to develop a project that automates these tedious steps, aiming to create a database for English vocabulary notes, which can also be integrated with other note sources.

## Problem to Solve

During the development of this project, we encountered some challenges that needed to be addressed:

1. How to use the Notion API?
2. What would be the best approach to implement this project: a web server, a browser extension, or an application?
3. How to design a web scraper to fetch word data from vocabulary websites (as using website APIs would be costly)?

## Project Overview

"vocabulary_database" is a project built using Python and Django framework, with the following main functionalities:

1. Utilize Selenium web scraper to automatically retrieve detailed information for specified words from the Cambridge English Dictionary website. This includes English definitions, Chinese translations, and related example sentences.
    
2. Automatically store the retrieved word information in Notion pages. Specifically, this feature allows users to add specified words, their definitions, translations, and example sentences to a Notion page.
    
3. Use Django models to organize and store word information. Specifically, there is a "Word" model for storing English words and their corresponding Chinese translations.
    

## Installation

To run this project, you need to install the necessary Python packages, including:

- Django==4.2.2 # Server
- beautifulsoup4==4.12.2 # Web scraper
- django-cors-headers==4.1.0 # Cross-origin request support
- requests==2.31.0 # Web scraper
- selenium==4.10.0 # Web scraper
- notion-client==2.0.0 # Notion API integration

You can install these packages by running the following command:

`pip install -r requirements.txt`

## Usage

To be updated by the author...

## Project Structure

This project is primarily divided into two parts: "vocabulary" and "cambridge."

- "vocabulary": This directory contains the Django project configuration files, such as settings.py, urls.py, etc.
    
- "cambridge": This directory contains the code related to fetching word data from the Cambridge website and storing it in the Notion database, including models.py, views.py, etc.
    

## Future Plans

We will continue to improve and expand this project to provide more features and a better user experience. Specific plans include:

1. Optimizing the efficiency and accuracy of word fetching.
2. Providing additional word sources beyond the Cambridge website.
3. Optimizing for spelling mistakes.
4. Improving the efficiency and accuracy of Notion data storage.

## Conclusion

Through this project, we aim to make the process of learning English smoother and more efficient. If you have any questions or suggestions, please feel free to contact us. Thank you for your attention and support!
