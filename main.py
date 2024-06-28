from typing import List
import openreview

# https://docs.openreview.net/getting-started/using-the-api/installing-and-instantiating-the-python-client
client = openreview.api.OpenReviewClient(
    baseurl="https://api2.openreview.net", username=EMAIL, password=PASSWORD
)

# https://docs.openreview.net/how-to-guides/data-retrieval-and-modification/how-to-get-all-submissions
# venue_group = client.get_group("NeurIPS.cc/2024/Conference")
# submission_name = venue_group.content["submission_name"]["value"]
# submissions = client.get_all_notes(invitation=f"NeurIPS.cc/2024/Conference/-/{submission_name}"")

# only get accepted submissions
submissions = client.get_all_notes(content={"venueid": "NeurIPS.cc/2024/Conference"})


def check_paper(keywords: List[str], abstract: str, WORD="neuroscience") -> bool:

    assert isinstance(keywords, list)
    assert isinstance(abstract, str)
    for keyword in keywords:
        if WORD in keyword:
            print(f"neuroscience in {keywords = }")
            return True

    if WORD in abstract:
        print(f"neuroscience in abstract")
        return True

    return False

counter = 0
for paper in submissions:
    content = paper.content
    # save all the keywords (in lower case) to a set
    keywords = [x.lower() for x in content["keywords"]["value"]]
    abstract = content["abstract"]["value"].replace("\n","")

    if not check_paper(keywords, abstract):
        continue

    title = content["title"]["value"]
    url = content["_bibtex"]["value"].split("url={")[-1].split("}")[0]
    author_str = ", ".join(content["authors"]["value"])
    print(author_str, title, abstract, url, sep="\n", end="\n\n")
    counter += 1
