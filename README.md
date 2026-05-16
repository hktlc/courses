# Hong Kong Seminary Course Catalogue 香港神學院課程目錄

A browsable HTML catalogue of theology courses offered by seminary schools in Hong Kong.  Users can filter courses by **level**, **theme**, **Bible book**, and **school**.

## Live Catalogue

Open `index.html` directly in a browser, or serve the repository root with any static-file server:

```bash
# Python 3
python -m http.server 8080
# then visit http://localhost:8080
```

## Project Structure

```
courses/
├── index.html          # Single-page HTML catalogue (frontend)
├── data/
│   └── courses.json    # Course database (JSON)
└── scraper/
    └── scraper.py      # Python scraper for live course data
```

## Course Database (`data/courses.json`)

Each entry in `courses.json` follows this schema:

| Field         | Type       | Description                                      |
|---------------|------------|--------------------------------------------------|
| `id`          | `string`   | Unique course ID, e.g. `"ABS-001"`               |
| `title_en`    | `string`   | Course title in English                          |
| `title_zh`    | `string`   | Course title in Chinese                          |
| `school`      | `string`   | Seminary name (English)                          |
| `school_zh`   | `string`   | Seminary name (Chinese)                          |
| `school_url`  | `string`   | Seminary website URL                             |
| `level`       | `string`   | `"seminar"` · `"entry"` · `"credit"` · `"degree"` |
| `themes`      | `string[]` | Topics, e.g. `["music", "counselling"]`          |
| `bible_books` | `string[]` | Relevant Bible books, e.g. `["Psalms", "Romans"]` |
| `description` | `string`   | Course description                               |
| `credits`     | `number`   | Credit hours (0 for non-credit seminars)         |
| `url`         | `string`   | Direct link to the course page                   |
| `semester`    | `string`   | e.g. `"2024 Fall"`                               |

### Levels

| Value      | Meaning                                  |
|------------|------------------------------------------|
| `seminar`  | Short courses, workshops, retreats       |
| `entry`    | Introductory / foundational courses      |
| `credit`   | Credit-bearing courses (non-degree)      |
| `degree`   | Full degree programmes (B.Th., M.Div., etc.) |

### Themes

Courses are tagged with one or more themes.  Currently used themes include:

`art` · `biblical studies` · `church history` · `church ministry` · `counselling` · `culture` · `ethics` · `family` · `languages` · `leadership` · `longevity` · `mental health` · `mission` · `music` · `pastoral ministry` · `psychology` · `research` · `social service` · `spiritual formation` · `theology` · `worship`

## Scraper (`scraper/scraper.py`)

The scraper is designed to fetch live course data from seminary websites and update `data/courses.json`.

### Install dependencies

```bash
pip install requests beautifulsoup4 lxml
```

### Run

```bash
# Scrape all schools (stubs will warn; activate by filling in selectors)
python scraper/scraper.py

# Scrape a single school
python scraper/scraper.py --school abs

# Preview output without writing to disk
python scraper/scraper.py --dry-run

# Replace courses.json entirely instead of merging
python scraper/scraper.py --no-merge
```

### Supported schools

| Key     | English Name                            | Chinese Name      |
|---------|-----------------------------------------|-------------------|
| `abs`   | Alliance Bible Seminary                 | 建道神學院        |
| `cgst`  | China Graduate School of Theology       | 中國神學研究院    |
| `lts`   | Lutheran Theological Seminary           | 信義宗神學院      |
| `evan`  | Evangel Seminary                        | 播道神學院        |
| `hkbts` | Hong Kong Baptist Theological Seminary  | 浸信會神學院      |
| `ccds`  | Chung Chi Divinity School (CUHK)        | 崇基學院神學組    |
| `gtc`   | Grace Theological College               | 恩福神學院        |
| `ats`   | Alliance Theological Seminary           | 宣道神學院        |

> **Note:** The per-school scraper functions in `scraper.py` are stubs.  To activate a scraper, inspect the target website's HTML structure and fill in the CSS selectors within the corresponding function.

## Contributing

1. Add new courses to `data/courses.json` following the schema above.
2. To implement a live scraper for a school, edit the relevant stub function in `scraper/scraper.py`.
3. Open a pull request with your changes.
