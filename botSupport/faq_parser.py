from bs4 import BeautifulSoup

def get_array(faqhtml):
    soap = BeautifulSoup(faqhtml, 'html.parser')
    for i in soap.find_all():
        print(i.contents[0])
