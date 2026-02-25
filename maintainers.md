# Guide for Maintainers on how to upload any new document

1. First, you should convert your word document into markdown file format. You can do this manually or easily with this online tool: https://word2md.com/
2. After you get the markdown file, you put the file inside the `src/docs` folder. Make sure the name of files should be in snake case.i.e. `File_Name.md`.
3. Add a json object at the end of `src/data/recent-work.json`. The format of json should look like this:

```json
{
    "id": should be unique id,
    "title": title of the file,
    "creator": author of the file,
    "type": type of the file,
    "time": time mentioned in the file,
    "class_size": class size mentioned in the file,
    "path": relative path of the file
}
```

4. After you do this, the code auto detects the new file and populates it into the recent work carousel.
