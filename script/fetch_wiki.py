import wikipedia

class WikiData:

    def get_wiki_corpus(self, search_text):
        titles = wikipedia.search(search_text)
        print(len(titles))

        wiki_content = []
        for title in titles:
            try:
                page = wikipedia.page(title)
                print("Title : ", page.title)
                page_content = page.content
                print(len(page_content))
                wiki_content.append(page_content)
            except wikipedia.exceptions.PageError:
                print(f"No page with -> {title}")
            except wikipedia.exceptions.DisambiguationError:
                print(f"Let's skip page")

        return wiki_content
