# Template layout

Two sites, two folders — nothing mixed at the root of `api/templates/`.

```
api/templates/
  learnhub/                 # notebook theme
    base.html
    home.html
    about.html
    topics.html
    topic_detail.html
    contact.html
    contact_success.html
  portfolio/                # dark theme
    shell.html              # all portfolio sections
```

| Site | Folder | Views render |
|------|--------|----------------|
| LearnHub | `learnhub/` | `learnhub/home.html`, … |
| Portfolio | `portfolio/` | `portfolio/shell.html` |

LearnHub pages: `{% extends 'learnhub/base.html' %}`  
Portfolio: single shell with `section` (home / work / skills / about / contact).
