# Online Mental Health Discourse  
By Roos Kuiper (14957876)  
  
*To view the formatted document in VS Code, press ctrl + shift + V*  
  
## Introduction  
This repository is part of an ongoing research project in which I investigate cultural and vernacular differences in online mental health discourse amongst platforms. By doing so, I aim to demonstrate how platform affordances affect online mental health discourse and impact visibility and representation. I wrote code to collect, process, and analyze data from Reddit, X (formerly Twitter), and LinkedIn. The file numbers remain constant despite loss of files throughout the coding pipeline, which makes is easy to navigate between these files in different stages of the data collection and processing. Running the code results in a small dataset of 660 posts, consisting of 3 subsets of 220 posts each, stored as plain text files to which transformer-based topic modelling can be applied.
  
## Setup and Running the Code  
**Create a virtual environment**:  
   ```  
   py -m venv .venv   
   ```  
**Activate the virtual environment**:  
   ```  
   .\.venv\Scripts\Activate.ps1  
   ```  
**Install dependencies**:  
   ```  
   pip -m install -r requirements.txt  
   ```  
I do not recommend running the scrapers, as doing so may change the dataset and result in different outcomes for the topic modelling. If you want to run the full pipeline anyways, I suggest running the LinkedIn scraper several times before continuing with parsing, normalization, and topic modelling. However, this process is time-intensive and unnecessary considering the dataset is already present in the project folder.  
  
**Run the scrapers**:  
   ```  
   .\S_auto.ps1  
   ```  
You can rerun the LinkedIn scraper by entering `py linkedin_scraping.py`.  
  
**Run the parsers and the code for normalization**:  
   ```  
   .\PN_auto.ps1  
   ```  
**Run the code for the topic modelling**:  
   ```  
   .\TM_auto.ps1  
   ```  
  
## URL Collection
While the initial plan was to collect URLs from each platform using the Brave Search API, this API has such severe limitations that it is not possible to collect the required number of URLs to conduct the research. Instead, I used a [Chrome extension](https://chromewebstore.google.com/detail/copy-all-urls-free/pnbocjclllbkfkkchadljokjclnpakia) to semi-automatically collect URLs by manually querying Google using search operators, clicking on each link and using the extension to copu the URLs from each open tab. I pasted the URLs to text documents (see: /data/urls_txt) which are loaded into the scrapers.  
  
I used the following queries for each platform:  
  
**Reddit**:  
site:https://www.reddit.com/r/*/comments/ intitle:"mental health"  
  
**X(/Twitter)**:  
site:https://x.com/*/status/ intitle:"mental health"  
  
**LinkedIn**:  
site:https://www.linkedin.com/posts/ intitle:"mental health"  
  
I adjusted the **Chrome settings** as follows:  
Display language: English  
Results language filter: English  
Results region: United States  
  
## Scripts  
You can find all individual scripts in the /src folder.  
  
**Scrapers**  
To collect the HTML code from each web page that corresponds to the collected URLs, I coded scrapers using [Playwright](https://playwright.dev/). To avoid getting flagged as suspicious by the platforms' anti-bot detection systems, I mimicked real user behaviour using a headed Chromium browser session rather than making raw HTTP requests, a user agent that makes requests appear to come from a regular desktop Chrome browser, randomized intervals between navigating to the web pages in order not to spam the servers, and using the same browser context while browsing the pages to make it look as if the pages are navigated to within one continuous browser session. I added a completion condition to make sure there are no more active network requests before the scraper captures the page. I also added a timeout after 60 seconds as a safeguard, so the code does not get stuck on a page that does not properly load. The URLs and HTML of the scraped web pages are stored as key-value pairs in separate JSON files (see: /data/html_json). In total, 796 web pages were collected, consisting of 265 Reddit pages, 283 X/Twitter pages, and 248 LinkedIn pages.  
  
**Parsers**   
To extract the posts, dates, and where relevant the post titles from the HTML sources, I coded parsers using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). I coded a function that iterates over all JSON files and created identifiers to find the parts of the HTML that contain the desired content and metadata. For X/Twitter and Linkedin, these identifiers refer to JSON-LD blocks inside the HTML, since the posts are trunkated in other parts of the HTML. Together with the URL, the extraction date and time, and the timezone, the posts, post titles, and upload dates are stored in new JSON documents (see: /data/post_json). I consciously did not extract any usernames, so users remain fully anonymous when they decide to remove their post. Only public and currently uploaded data will show when a web page in the dataset is navigated to.  
  
**Normalization**  
To get a uniform dataset that is suitable for topic modelling, I coded scripts for normalizing the data. The functions in these scripts extract posts and, in the case of Reddit, post titles and convert them to text files. Post title extraction is unnecessary for posts on X and LinkedIn, since posts on X don't contain post titles and titles of posts on LinkedIn are identical to the first line of the post itself. The functions limit conversion to 220 documents to have an equal number of documents per platform for the topic modelling. The text files are stored in /data/post_txt.  
  
**Topic Modelling**  
For the topic modelling I make use of [BERTopic](https://bertopic.readthedocs.io/en/latest/), which is a Python library meant to create a pipeline of models for transformer-based topic modelling. BERTopic is especially useful for noisy, short-form texts like social media posts due to its use of semantic embeddings rather than relying on word co-occurrence alone. The pipeline consists of an embedding model, a dimensionality reduction model, a clustering model, a vectorizer model, and a topic extraction model. I chose not to use the standard representation model, since this model has a tendency to remove abbreviations and other vernacularly relevant topic words from the topic word representations. 
  
**Visualizations**  
For the visualizations, I generated document cluster maps to demonstrate the relations between documents and aid in identifying overarching themes in and overlap between topics. These maps are available as interactive [Plotly](https://docs.plotly.com/) figures using HTML as well as static PNG images (see: /output/figures).  
  
## Results

(Under construction...)
   
To view the interactive figures, you can ctrl + click on the links below, then right-click the file name at the top and click "Open in Integrated Browser"  
  
[Reddit documents visualization (interactive)](.\output\figures\reddit_documents.html)  
[X/Twitter documents visualization (interactive)](.\output\figures\twitter_documents.html)  
[LinkedIn documents visualization (interactive)](.\output\figures\linkedin_documents.html)  
  
**Reddit**  
![Reddit documents visualization (static)](.\output\figures\reddit_documents.png) 
*Reddit documents visualization (static)*
    
| Topic nr. | File count | BERTopic label | Alternative label | Topic words |  
| --- | --- | --- | --- | --- |  
| -1 | 42 | members_counseling_care_relationship | outliers/noise | 'members', 'counseling', 'care', 'relationship', 'immediate', 'demand', 'access', 'read', 'treatment', 'member' |  
| 0 | 22 | insurance_resources_affordable_looking | resources | 'insurance', 'resources', 'affordable', 'looking', 'afford', 'income', 'services', 'info', 'area', 'tried' |  
|1 | 16 | medication_shared_medications_horrible | experiences and advice | 'medication', 'shared', 'medications', 'horrible', 'quickly', 'continue', 'check', 'effects', 'housing', 'doing' |  
| 2 | 14 | sick_days_phd_leave | work and education | 'sick', 'days', 'phd', 'leave', 'taken', 'year', 'stop', 'feeling', 'taking', 'day' |
| 3 | 14 | friend_child_crisis_services | helping a loved one | 'friend', 'child', 'crisis', 'services', 'families', 'suicidal', 'family', 'program', 'severe', 'appreciate' |  
| 4 | 12 | character_player_characters_fun | entertainment | 'character', 'player', 'characters', 'fun', 'control', 'dead', 'weight', 'eyes', 'healthcare', 'playing' |  
| 5 | 11 | game_playing_character_campaign | games | 'game', 'playing', 'character', 'campaign', 'player', 'players', 'session', 'play', 'dm', 'research' |  
| 6 | 10 | tech_career_licensed_projects | careers in mental health | 'tech', 'career', 'licensed', 'projects', 'science', 'field', 'working', 'understand', 'psych', 'grad' |  
| 7 | 10 | private_practice_cmh_paying | mental health systems | 'private', 'practice', 'cmh', 'paying', 'clients', 'community', 'unless', 'pay', 'therapists', 'staff' |  
| 8 | 10 | fantasy_writing_characters_series | literature and fiction | 'fantasy', 'writing', 'characters', 'series', 'reading', 'representation', 'real', 'theory', 'haven', 'problems' |  
| 9 | 9 | concept_illness_environment_ability | defining mental health | 'concept', 'illness', 'environment', 'ability', 'include', 'happy', 'exactly', 'mean', 'individual', 'mentally' |  
| 10 | 8 | inpatient_facility_facilities_recommendations | local facilities | 'inpatient', 'facility', 'facilities', 'recommendations', 'phone', 'considering', 'denver', 'highly', 'avoid', 'outside' |
| 11 | 7 | doctor_therapy_discussion_aa | therapy | 'doctor', 'therapy', 'discussion', 'aa', 'insight', 'chance', 'lost', 'normal', 'hell', 'helps' |  
| 12 | 7 | loneliness_connect_negative_periods | loneliness | 'loneliness', 'connect', 'negative', 'periods', 'felt', 'small', 'friends', 'thoughts', 'hope', 'connections' |  
| 13 | 7 | ai_class_school_students | students | 'ai', 'class', 'school', 'students', 'video', 'cut', 'studying', 'weren', 'student', 'sent' |  
| 14 | 7 | performance_results_running_motivation | exercise | 'performance', 'results', 'running', 'motivation', 'study', 'benefits', 'positive', 'exercise', 'brain', 'stress' |    
| 15 | 7 | men_awareness_month_suffer | men's mental health | 'men', 'awareness', 'month', 'suffer', 'reach', 'stand', 'talked', 'remember', 'joy', 'ignored' |  
| 16 | 7 | minutes_client_left_company | career struggles | 'minutes', 'client', 'left', 'company', 'stress', 'got', 'crisis', 'worked', 'large', 'center' |  
  
**X(/Twitter)**  
![X/Twitter documents visualization (static)](.\output\figures\twitter_documents.png)  
*X/Twitter documents visualization (static)*
  
| Topic nr. | File count | BERTopic label | Alternative label | Topic words |  
| --- | --- | --- | --- | --- |  
| -1 | 55 | conversations_provide_proud_speak | outliers/noise | 'conversations', 'provide', 'proud', 'speak', 'public', 'professionals', 'supporting', 'week', 'department', 'issues' |  
| 0 | 17 | matter_school_schools_action | ... | 'matter', 'school', 'schools', 'action', 'events', 'black', 'students', 'awareness', 'communities', 'children' |  
| 1 | 15 | journey_mham2026_person_create | ... | 'journey', 'mham2026', 'person', 'create', '25', 'samhsa', 'behavioral', 'community', 'share', 'confidential' |  
| 2 | 15 | guide_samhsa_county_symptoms | ... | 'guide', 'samhsa', 'county', 'symptoms', 'use', 'mentalhealthmonth', 'disorder', 'tools', 'treatment', 'know' |  
| 3 | 12 | nyc_yorkers_new_real | ... | 'nyc', 'yorkers', 'new', 'real', 'state', 'access', 'live', 'chat', 'substance', 'use' |  
| 4 | 12 | research_country_local_including | ... | 'research', 'country', 'local', 'including', 'read', 'condition', 'act', 'communities', 'bit', 'calling' |  
| 5 | 11 | women_seek_problems_tips | ... | 'women', 'seek', 'problems', 'tips', 'challenges', 'face', 'bit', 'matters', 'vital', 'understand' |  
| 6 | 11 | self_explore_barriers_online | ... | 'self', 'explore', 'barriers', 'online', 'improve', 'tools', 'reach', 'conditions', 'different', 'judgment' |  
| 7 | 9 | practice_moment_make_mind | ... | 'practice', 'moment', 'make', 'mind', 'wellbeing', 'young', 'children', 'selfcare', 'reflect', 'sharing' |  
| 8 | 8 | reminds_watch_tips_way | ... | 'reminds', 'watch', 'tips', 'way', 'understanding', 'building', 'taking', 'visit', 'conditions', 'mentalhealthawarenessmonth' |  
| 9 | 7 | stigma_week_crucial_fostering | ... | 'stigma', 'week', 'crucial', 'fostering', 'attend', 'job', 'group', 'opening', 'ow', 'impact' |  
| 10 | 7 | sites_national_24_experience | ... | 'sites', 'national', '24', 'experience', 'women', 'confidential', 'challenges', 'program', 'vital', 'strong' |  
| 11 | 7 | suicide_crisis_prevention_talk | ... | 'suicide', 'crisis', 'prevention', 'talk', 'struggling', 'chat', 'episode', 'thoughts', 'abuse', 'substance' |  
| 12 | 7 | link_apply_fostering_based | ... | 'link', 'apply', 'fostering', 'based', 'provides', 'response', 'sharing', 'tinyurl', 'silence', 'practice' |  
| 13 | 7 | discussion_ages_development_crucial | ... | 'discussion', 'ages', 'development', 'crucial', 'want', 'making', 'science', 'priority', 'research', '10' |  
| 14 | 7 | mind_science_disorders_body | ... | 'mind', 'science', 'disorders', 'body', 'real', 'key', 'affects', 'check', 'com', 'social' |  
| 15 | 7 | day_worldmentalhealthday_world_let | ... | 'day', 'worldmentalhealthday', 'world', 'let', 'prioritize', 'matters', 'development', 'break', 'resilience', 'navigate' |  
| 16 | 6 | means_experiencing_insurance_link | ... | 'means', 'experiencing', 'insurance', 'link', 'behavioral', 'physical', 'barriers', 'way', 'reach', 'anxiety' |  
  
  
**LinkedIn**  
![LinkedIn documents visualization (static)](.\output\figures\linkedin_documents.png)  
 *LinkedIn documents visualization (static)*
   
| Topic nr. | File count | BERTopic label | Alternative label | Topic words |  
| --- | --- | --- | --- | --- |   
| -1 | 69 | medication_psychiatric_like_use | outliers/noise | 'medication', 'psychiatric', 'like', 'use', 'brain', 'conversation', 'behavioral', 'group', 'family', 'resources' |  
| 0 | 24 | digital_data_article_media | ... | 'digital', 'data', 'article', 'media', 'clinical', 'effective', 'insights', 'innovation', 'content', 'lived' |  
| 1 | 13 | planning_review_interventions_severe | ... | 'planning', 'review', 'interventions', 'severe', 'advance', 'treatments', 'global', 'change', 'evidence', 'countries' |  
| 2 | 13 | early_young_youth_children | ... | 'early', 'young', 'youth', 'children', 'begin', 'schools', 'california', 'peer', 'concerns', '25' |  
| 3 | 10 | month_environments_reminder_supported | ... | 'month', 'environments', 'reminder', 'supported', 'able', 'awareness', 'performance', 'reflects', 'ongoing', 'conversations' |  
| 4 | 10 | kids_activities_hosted_events | ... | 'kids', 'activities', 'hosted', 'events', 'families', 'child', 'grateful', 'day', 'walk', 'supported' |  
| 5 | 10 | city_office_law_director | ... | 'city', 'office', 'law', 'director', 'individuals', 'provides', 'wellness', 'york', 'community', 'programs' |  
| 6 | 9 | employees_workplace_report_financial | ... | 'employees', 'workplace', 'report', 'financial', 'asking', 'burnout', 'stress', 'believe', 'cycle', 'claims' |  
| 7 | 8 | board_safety_settings_carers | ... | 'board', 'safety', 'settings', 'carers', 'service', 'rights', 'informed', 'model', 'blog', 'grounded' |  
| 8 | 7 | student_counseling_california_higher | ... | 'student', 'counseling', 'california', 'higher', 'case', 'year', 'continues', 'institutions', 'college', 'education' |  
| 9 | 7 | 988_disorder_24_division | ... | '988', 'disorder', '24', 'division', 'common', 'develop', 'life', 'session', 'suicide', 'come' |  
| 10 | 7 | insurance_women_sustained_safe | ... | 'insurance', 'women', 'sustained', 'safe', 'engagement', 'symptoms', 'healthy', 'does', 'embedded', 'coverage' |  
| 11 | 7 | research_webinar_ireland_looking | ... | 'research', 'webinar', 'ireland', 'looking', 'sector', 'development', 'implementation', 'lived', 'learning', 'workforce' |  
| 12 | 6 | right_government_pathways_options | ... | 'right', 'government', 'pathways', 'options', 'justice', 'single', '20', 'better', 'invest', 'stability' |  
| 13 | 5 | practice_trained_medicine_performance | ... | 'practice', 'trained', 'medicine', 'performance', 'paper', 'university', 'state', 'professional', 'coaching', 'standard' |  
| 14 | 5 | participation_prevention_analysis_initiative | ... | 'participation', 'prevention', 'analysis', 'initiative', 'equity', 'investing', 'integrated', 'healthy', 'adolescents', 'mechanisms' |  
| 15 | 5 | stigma_barriers_center_local | ... | 'stigma', 'barriers', 'center', 'local', 'primary', 'isolation', 'end', 'times', 'low', 'financial' |  
| 16 | 5 | region_2026_12_april | ... | 'region', '2026', '12', 'april', 'march', 'wednesday', 'framework', 'meeting', 'tuesday', 'registration' |  
  
## AI Disclosure Statement  
For this research project, I used ChatGPT to explain traceback calls, identify compatibility problems and syntax errors, identify the correct HTML elements for the parsers, and set up a basic structure for the scrapers. Since the scripts for each platform follow a similar structure, much of the code could be reused with small alterations. I did **not** use AI to generate any of the written components in this project.  