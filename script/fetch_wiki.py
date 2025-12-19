from langchain_core.documents import Document
import wikipedia

class WikiData:

    def get_wiki_corpus(self, search_text):
        titles = wikipedia.search(search_text)
        print(len(titles))

        documents = []
        for title in titles:
            try:
                page = wikipedia.page(title)

                documents.append(
                    Document(
                        page_content=page.content,
                        metadata={
                            "source": "wikipedia",
                            "title": page.title,
                            "url": page.url,
                            "page_id": page.pageid,
                            "search_query": search_text

                        }
                    )
                )

            except wikipedia.exceptions.PageError:
                print(f"No page with -> {title}")
            except wikipedia.exceptions.DisambiguationError:
                print(f"Let's skip page")

        return documents
