&lt;links /&gt;
=========

A simple as possible link shortener/tracker, meant for easy web-service integration.

(Partial) tech list:

+ Python 3
    + Flask
    + SQLAlchemy
    + WTForms
+ Postgres
+ Bootstrap 4
+ FontAwesome 4

Activate the venv & load the env vars:
```bash
source .venv/bin/activate
export $(cat *.env | grep "^[^#;]" | xargs)
```

First time use:
+ `python -m links db init`
+ Add `import sqlalchemy_utils` and `from sqlalchemy import Text` to `migrations/script.py.mako`
+ `python -m links db migrate`
+ `python -m links db upgrade`

Licence
-------

Copyright 2017 Dries007

Licensed under the EUPL, Version 1.2 only (the "Licence");<br/> 
You may not use this work except in compliance with the Licence.<br/>
You may obtain a copy of the Licence, available in 23 official languages of the European Union, at:

+ https://joinup.ec.europa.eu/community/eupl/og_page/eupl-text-11-12
+ For your convenience, a copy of the english text is available in [LICENCE.txt](LICENCE.txt)

Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.<br/>
See the Licence for the specific language governing permissions and limitations under the Licence.
