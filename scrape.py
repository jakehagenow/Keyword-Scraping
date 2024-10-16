from bs4 import BeautifulSoup
import requests 
import re 

def scrape_website(website, keywords):
    keywords = keywords.split(',')

    print("Launching BeautifulSoup...")

    result = requests.get(website)
    html = BeautifulSoup(result.content, "html.parser")

    # print(html)

    important_elements = ["h1", "h2", "h3", "p", "ul", "ol", "a", "strong", "b", "em", "i"]

    text = ""
    links = []
    of_note = []

    for tag in important_elements:
        elements = html.find_all(tag)

        for element in elements:
        
            text += element.text.strip()# + "\n"

            for word in keywords:
                if word.lower() in element.text.lower():
                    of_note.append(element.text.strip())
                
            if tag == "a" and "href" in element.attrs:
                link = element.attrs["href"]

                if link[0] == '/': 
                    links.append(f"{website}{link}")
                
                else:
                    links.append(link)

                for word in keywords:
                    if word.lower() in link.lower():
                        of_note.append(f"{website}{link}")     

    return {
        "text": text,
        "found": of_note,
        "links": links,
        "title": html.title.text,
        "url": website,
    }

def create_prompt(summary):
    print("In prompt creation...")
    template = f"""
    Summarize the information found in a list of website sections.

  Args:
      data: A list of lists, where each inner list represents a section of the
          website data output. The elements can be made up of text, titles, and links.

  Return:
      A table that includes the main points found in the text of the arguments. Please also elaborate on any of the other points if you are confident that you have helpful information on the subject.

  Here is the data: 
      {summary}
"""
    print(template)
    return template

