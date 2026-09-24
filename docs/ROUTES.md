# Routes — LearnHub vs Portfolio

No shared paths. Each site has its own prefix and templates.

## LearnHub (notebook theme → `base.html`)

| URL | Name | View |
|-----|------|------|
| `/` | `home` | LearnHub home |
| `/home/` | `home_page` | same |
| `/topics/` | `topics` | topic list |
| `/topics/<id>/` | `topic_detail` | topic detail |
| `/about/` | `about` | LearnHub about |
| `/contact/` | `contact` | LearnHub contact form |
| `/contact/success/` | `contact_success` | success |

## Portfolio (dark theme → `portfolio.html`)

| URL | Name | View |
|-----|------|------|
| `/portfolio/` | `portfolio` | portfolio home |
| `/portfolio/work/` | `portfolio_work` | work |
| `/portfolio/skills/` | `portfolio_skills` | skills |
| `/portfolio/about/` | `portfolio_about` | about |
| `/portfolio/contact/` | `portfolio_contact` | portfolio contact form |
| `/portfolio/contact/success/` | `portfolio_contact_success` | success |

## Contact data

Both forms POST to their **own** URL but call the same save helper → **Profiles** + **Contacts** in admin.

## Do not

- Link portfolio nav to `/contact/` or `/about/`
- Link LearnHub nav to `/portfolio/contact/` for primary contact (footer cross-link is fine)
- Add root `/work/` or `/skills/` again (removed to avoid dual entry)
