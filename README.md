# LessWrong PDF Exporter

This is a quick Python script, which uses the [GraphQL endpoint](https://www.lesswrong.com/posts/LJiGhpq8w4Badr5KJ/graphql-tutorial-for-lesswrong-and-effective-altruism-forum) to download the Markdown for a post, and then calls pandoc to export to a PDF.

I have no plans to support/develop this script, and the LessWrong developers can probably throw together something much better.

This may be useful if you either want to quickly print a post for personal reading, and "good enough" is fine. You can also clean up the markdown (or pandoc-converted latex) manually if you want something more polished (e.g. a PDF you want to share).

There are a few examples of exported PDFs in `out/`.

Example usage:
```
python3 get_markdown.py --post_id=2mhFMgtAjFJesaSYR
```
