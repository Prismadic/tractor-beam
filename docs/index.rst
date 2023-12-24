.. tractor_beam documentation master file, created by
   sphinx-quickstart on Sat Dec 23 16:09:53 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. raw:: html

   <h1 align="center">

   Welcome to the 🛸 docs

.. raw:: html

   </h1>

|DIV|

.. toctree::
   :maxdepth: 3
   :caption: Packages & useful classes

   tractor_beam.clone	
   tractor_beam.laser
   tractor_beam.telepathy	
   tractor_beam.lab	
   tractor_beam.visits	
   tractor_beam.utils

.. raw:: html

   <h3 align="center">

high-efficiency text & file scraper with smart tracking

.. raw:: html

   </h3>

🧬 Installation
----------------

|DIV|

.. code:: bash

   pip install llm-tractor-beam

or

.. code:: bash

   python3 setup.py install

⚡️ usage
=======

|DIV|

🛸 check .json configs!

.. raw:: html

   <details>

.. raw:: html

   <summary>

   Single File

.. raw:: html

   </summary>

.. code:: python

   from tractor_beam import beam
   auto = tractor_beam.tractor_beam('./config.json')
   run = auto.go()
   print(run)
   auto.destroy('example')

.. code:: shell

   🌊 SUCCESS: config set from - ./example.json
   ℹ️ INFO: config saved to - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/example
   🌊 SUCCESS: unboxed! 🛸📦 - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/example 
   ☕️ WAIT: tractor beaming with "example"
   ℹ️ INFO: Abduct initialized
   ℹ️ INFO: Records initialized
   ℹ️ INFO: Focus initialized
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/example/fomchistorical2017.htm
   [{'file': 'https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm', 'path': '/Users/dylanmoore/VSCode/LLM/tractor-beam.git/example/fomchistorical2017.htm'}]
   ☕️ WAIT: setting header with `.keys()`
   🌊 SUCCESS: headers detected as ['file', 'path'] from `.keys()`
   ℹ️ INFO: created /Users/dylanmoore/VSCode/LLM/tractor-beam.git/example/receipts.csv
   ℹ️ INFO: timestamped - 2023-09-05 06:36:57.003699
   🌊 SUCCESS: 1 written to /Users/dylanmoore/VSCode/LLM/tractor-beam.git/example/receipts.csv
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/example/fomchistorical2017_cleaned.txt
   🌊 SUCCESS: 🛸 done
   {'config': <tractor_beam.config.Config object at 0x10fde00d0>, 'copier': <tractor_beam.clone.replicator.Abduct object at 0x10e588d50>, 'receipts': <tractor_beam.visits.sites.Records object at 0x10fddb0d0>, 'janitor': <tractor_beam.janitor.Focus object at 0x106c6af90>, 'data': [{'file': 'https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm', 'path': '/Users/dylanmoore/VSCode/LLM/tractor-beam.git/example/fomchistorical2017.htm', 'ts': datetime.datetime(2023, 9, 5, 6, 36, 57, 3699)}], 'status': 'complete'}
   🚨 WARN: example destroyed

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   Recursive/Batch Processing

.. raw:: html

   </summary>

.. code:: python

   from tractor_beam import beam
   auto = tractor_beam.tractor_beam('./recurse.example.json')
   run = auto.go()
   print(run)
   auto.destroy('recurse_example')

.. code:: shell

   🌊 SUCCESS: config set from - ./recurse.example.json
   ℹ️ INFO: config saved to - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example
   🌊 SUCCESS: unboxed! 🛸📦 - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example 
   ☕️ WAIT: tractor beaming with "recurse_example"
   ℹ️ INFO: Abduct initialized
   ℹ️ INFO: Records initialized
   ℹ️ INFO: Focus initialized
   ☕️ WAIT: processing https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm
   100%|██████████| 326/326 [00:00<00:00, 196344.50it/s]
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/beigebook/files/Beigebook_20170118.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170201tealbooka20170123.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170201tealbookb20170126.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170201Agenda.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC_LongerRunGoals_201701.pdf
   ...
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170503tealbookb20170427.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170503Agenda.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/fomcminutes20170503.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170503meeting.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170503material.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/BeigeBook_20170531.pdf
   ...
   ℹ️ INFO: timestamped - 2023-09-05 06:41:52.462400
   ℹ️ INFO: timestamped - 2023-09-05 06:41:52.462402
   🌊 SUCCESS: 65 written to /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/receipts.csv
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/Beigebook_20170118_cleaned.txt
   Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20170201tealbooka20170123_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20170201tealbookb20170126_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20170201Agenda_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC_LongerRunGoals_201701_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/fomcminutes20170201_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20170201meeting_cleaned.txt
   ...
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20170503tealbooka20170421_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20170503tealbookb20170427_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20170503Agenda_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/fomcminutes20170503_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20170503meeting_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20170503material_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/BeigeBook_20170531_cleaned.txt
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20170614tealbooka20170605_cleaned.txt
   ...
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/recurse_example/FOMC20171213material_cleaned.txt
   🌊 SUCCESS: 🛸 done
   {'config': <tractor_beam.config.Config object at 0x105301a10>, 'copier': <tractor_beam.clone.replicator.Abduct object at 0x1041c3390>, 'receipts': <tractor_beam.visits.sites.Records object at 0x106792690>, 'janitor': <tractor_beam.janitor.Focus object at 0x106792c90>, 'data': [{'file': 'https://www.federalreserve.gov/monetarypolicy/beigebook/files/Beigebook_20170118.pdf'...
   🚨 WARN: recurse_example destroyed

.. raw:: html

   </details>

   old (many of these will be broken while being retrofitted)

.. raw:: html

   <details>

.. raw:: html

   <summary>

   single file & receipt creation, then deletion

.. raw:: html

   </summary>

.. code:: python

   from tractor_beam.clone.replicator import Abduct
   from tractor_beam.visits.sites import Records
   data = []
   copy = Abduct(url='https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm')
   if copy.download('./fed.txt'):
       data.append({"file":copy.url, "path":f'{copy.path}'})
   receipts = Records(path='./fed.csv', data=data)
   receipts.create(True)
   receipts.write(False)
   copy.destroy(confirm=copy.path.split('/')[-1])
   receipts.destroy(confirm=receipts.path.split('/')[-1])

.. code:: shell

   ℹ️ INFO: written - ./fed.txt
   ☕️ WAIT: no header set - attempting `.keys()`
   🌊 SUCCESS: headers detected as ['file', 'path'] from `.keys()`
   ℹ️ INFO: [file, path, ts] header used
   ℹ️ INFO: created ./fed.csv
   ℹ️ INFO: timestamped - 2023-08-31 17:07:19.544208
   🌊 SUCCESS: 1 written to ./fed.csv
   🚨 WARN: fed.txt destroyed from ./fed.txt
   🚨 WARN: fed.csv destroyed from ./fed.csv

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   seek through receipts

.. raw:: html

   </summary>

.. code:: python

   integer = receipts.seek(line=0)
   string = receipts.seek(line='monetarypolicy')
   by_date = receipts.seek(line='2023-08-31')
   print(integer)
   print(string)
   print(by_date)

.. code:: shell

   ℹ️ INFO: found monetarypolicy in data
   ℹ️ INFO: found 2023-08-31 in data
   {'file': 'https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm', 'path': './fed.txt', 'ts': '2023-08-31 19:57:02.593086'}
   [{'file': 'https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm', 'path': './fed.txt', 'ts': '2023-08-31 19:57:02.593086'}]
   [{'file': 'https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm', 'path': './fed.txt', 'ts': '2023-08-31 19:57:02.593086'}]

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   recursive mode with three filetypes, and whole directory deletion

.. raw:: html

   </summary>

.. code:: python

   from tractor_beam.clone.replicator import Abduct
   from tractor_beam.visits.sites import Records

   copy = Abduct(url='https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm', recurse=True)
   data=[]
   files = copy.download('./fed', types=['csv','xml','pdf'])[0]
   for file in files:
       data.append({"file":file, "path":f'{copy.path}/{file.split("/")[-1]}'})
   receipts = Records('./fed.csv', data=data)
   receipts.create(False)
   receipts.write(False)
   copy.destroy(confirm=copy.path.split('/')[-1])
   receipts.destroy(confirm=receipts.path.split('/')[-1])

.. code:: shell

   ☕️ WAIT: processing https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm
   100%|██████████| 326/326 [00:00<00:00, 154066.83it/s]
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/beigebook/files/Beigebook_20170118.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170201tealbooka20170123.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20170201tealbookb20170126.pdf
   ...
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20171213SEPcompilation.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20171213SEPkey.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20171213meeting.pdf
   ℹ️ INFO: found - https://www.federalreserve.gov/monetarypolicy/files/FOMC20171213material.pdf

   Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

   ℹ️ INFO: written - ./fed/Beigebook_20170118.pdf
   ℹ️ INFO: written - ./fed/FOMC20170201tealbooka20170123.pdf
   ℹ️ INFO: written - ./fed/FOMC20170201tealbookb20170126.pdf
   ℹ️ INFO: written - ./fed/FOMC20170201Agenda.pdf
   ℹ️ INFO: written - ./fed/FOMC_LongerRunGoals_201701.pdf
   ℹ️ INFO: written - ./fed/fomcminutes20170201.pdf
   ℹ️ INFO: written - ./fed/FOMC20170201meeting.pdf
   ℹ️ INFO: written - ./fed/FOMC20170201material.pdf
   ℹ️ INFO: written - ./fed/Beigebook_20170301.pdf
   ℹ️ INFO: written - ./fed/FOMC20170315tealbooka20170303.pdf
   ℹ️ INFO: written - ./fed/FOMC20170315tealbookb20170309.pdf
   ℹ️ INFO: written - ./fed/FOMC20170315Agenda.pdf
   ...
   ℹ️ INFO: timestamped - 2023-08-31 16:40:37.573578
   🌊 SUCCESS: 65 written to ./fed.csv
   🚨 WARN: 65 destroyed from ./fed
   🚨 WARN: fed.csv destroyed from ./fed.csv

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   example custom anonymous function

.. raw:: html

   </summary>

.. code:: python

   from tractor_beam.supplies import Custom
   data = 'linkbase:hello there'
   SECSifter = Custom(copy=data)

   SECSifter.sift = lambda _: '' if _.startswith('linkbase:') else _

   sifted = SECSifter.sift(data)
   print(sifted)

.. code:: shell

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   rendering markdown handler

.. raw:: html

   </summary>

.. code:: python

   data = '<html>hello there</html>'
   from tractor_beam.supplies import Strip
   clean = Strip(copy=data).sanitize()
   print(clean)
   xml = '<TITLE>hello there</TITLE>'
   clean = Strip(copy=xml).sanitize(xml=True)
   print(clean)

.. code:: shell

   hello there
   TITLE: hello there

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   pure text formatter

.. raw:: html

   </summary>

.. code:: python

   from tractor_beam.janitor import Focus
   worker = Focus(path='./fed.txt', o='./fed_processed.txt')
   worker.process()
   worker.destroy(confirm=worker.o.split('/')[-1])

.. code:: shell

   ℹ️ INFO: written - ./fed_processed.txt
   🚨 WARN: fed_processed.txt destroyed from ./fed_processed.txt

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   dataset statistics

.. raw:: html

   </summary>

.. code:: python

   from tractor_beam.teacher import SP

   copy = './fed.txt'
   save='./plot.png'

   p = SP(copy, save)
   p.generate(show=True)
   p.destroy(confirm=p.save.split('/')[-1])

.. figure:: plot.png
   :alt: SP

   SP

.. code:: shell

   🚨 WARN: plot.png destroyed from ./plot.png

.. raw:: html

   </details>


🤓 advanced configuration & job planning (many of these will be broken while being retrofitted)
-----------------------------------------------------------------------------------------------

.. raw:: html

   <details>

.. raw:: html

   <summary>

   declare existing config from file

.. raw:: html

   </summary>

.. code:: python

   from tractor_beam.config import Config
   example = Config("./config.json")


.. code:: python

   conf = example.use()
   _l = lambda _: list(_)
   print(_l(conf.keys()))
   print(conf["settings"]["name"])


.. code:: python

   conf["settings"]["name"] = 'example'
   example.save()

remove from memory
~~~~~~~~~~~~~~~~~~

.. code:: python

   c, conf = (None, None)

load from f/s again
~~~~~~~~~~~~~~~~~~~

.. code:: python

   c = Config("./config.json")
   conf = c.use()
   role, name = conf['role'], conf['settings']['name']

see that the value has changed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   print(f'{role}: {name}')

.. code:: shell

   🌊 SUCCESS: config loaded from - ./config.json
   ['role', 'settings']
   fin-tractor_beam
   🌊 SUCCESS: config saved to - ./config.json (overwrite)
   🌊 SUCCESS: config loaded from - ./config.json
   server: example

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   overrides

.. raw:: html

   </summary>

.. code:: python

   example.unbox(True)
   example.unbox()
   example.destroy()

.. code:: shell

   🌊 SUCCESS: unboxed! 🛸📦 - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/example 
   ☠️ FATAL: exists - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/example
   🚨 WARN: example destroyed

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   initialize from memory i.e. API response

.. raw:: html

   </summary>

.. code:: python

   fin_conf = {
       "role": "server",
       "settings": {
           "name": "fin-tractor_beam",
           "proj_dir": "/Users/dylanmoore/VSCode/LLM/tractor-beam.git/",
           "jobs": [
               {
                   "url": "https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm",
                   "types": [],
                   "janitor": 0,
                   "custom": [
                       {
                           "func": ""
                           , "types": [""]
                       }
                   ]
               }
           ]
       }
   }
   direct_load = Config(fin_conf)
   direct_load.use()
   direct_load.destroy('fin-tractor_beam')

.. code:: shell

   🌊 SUCCESS: unboxed! 🛸📦 using - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/fin-tractor_beam 
   🌊 SUCCESS: config loaded from - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/fin-tractor_beam/config.json
   🚨 WARN: fin-tractor_beam destroyed

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   all together now 🎶

.. raw:: html

   </summary>

.. code:: python

   # all together now 🎶
   from tractor_beam.clone.replicator import Abduct
   from tractor_beam.visits.sites import Records
   from tractor_beam.config import Config
   from tractor_beam.janitor import Focus
   import os

   fin_conf = {
       "role": "server",
       "settings": {
           "name": "fin-tractor_beam",
           "proj_dir": "/Users/dylanmoore/VSCode/LLM/tractor-beam.git/",
           "jobs": [
               {
                   "url": "https://www.federalreserve.gov/monetarypolicy/fomchistorical2017.htm",
                   "types": [],
                   "janitor": 0,
                   "custom": [
                       {
                           "func": ""
                           , "types": [""]
                       }
                   ]
               }
           ]
       }
   }
   direct_load = Config(fin_conf)
   c = direct_load.use()
   p = os.path.join(c['settings']['proj_dir'], c['settings']['name'])
   data = []
   for job in c['settings']['jobs']:
       copy = Abduct(url=job['url'])
       if copy.download(p+'/fed.txt'):
           data.append({"file":copy.url, "path":f'{copy.path}'})
   receipts = Records(path=p+'/fed.csv', data=data)
   receipts.create(True)
   receipts.write(False)
   worker = Focus(p+'/fed.txt', o=p+'/fed_processed.txt')
   worker.process()

.. code:: shell

   🌊 SUCCESS: unboxed! 🛸📦 using - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/fin-tractor_beam 
   🌊 SUCCESS: config loaded from - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/fin-tractor_beam/config.json
   ℹ️ INFO: written - /Users/dylanmoore/VSCode/LLM/tractor-beam.git/fin-tractor_beam/fed.txt
   🚨 WARN: path not found
   ☕️ WAIT: no header set - attempting `.keys()`
   🌊 SUCCESS: headers detected as ['file', 'path'] from `.keys()`
   ℹ️ INFO: [file, path, ts] header used
   ℹ️ INFO: created /Users/dylanmoore/VSCode/LLM/tractor-beam.git/fin-tractor_beam/fed.csv
   ℹ️ INFO: timestamped - 2023-09-01 17:28:27.786525
   🌊 SUCCESS: 1 written to /Users/dylanmoore/VSCode/LLM/tractor-beam.git/fin-tractor_beam/fed.csv

.. raw:: html

   </details>

.. raw:: html

   <details>

.. raw:: html

   <summary>

   💣

.. raw:: html

   </summary>

.. code:: python

   # that easy
   direct_load.destroy('fin-tractor_beam')

.. code:: shell

   🚨 WARN: fin-tractor_beam destroyed

.. raw:: html

   </details>

|DIV|

📝 needs
----------------

   - worker/server engineering

      - finish ``Fax`` -> ``NATS docs <https://natsbyexample.com>``, ``py
         client <https://github.com/nats-io/nats.py>``

   - good readme

   - config template / management

      - optional encryption of config unboxings

   - tests 😢

      - move more to ``.utils``

      - if / ternary conventions

   - implement API response option for ``Abduct``

      - custom header arg for ``Abduct``

   - add multiprocessing where needed

      - put ``tqdm`` in the right places

.. raw:: html

   <h3 align="center">

learn more about how Prismadic uses 🛸

subscribe to our `substack <https://prismadic.substack.com>`_

.. raw:: html

   </h3>


|A1| |A2|

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |A1| image:: https://github.com/Prismadic/.github/raw/main/profile/image_square.jpg
.. |A2| image:: https://github.com/Prismadic/.github/raw/main/profile/accent_color_square.jpg
.. |DIV| image:: https://github.com/Prismadic/magnet/raw/ef68535ecee236ff007638afa56de538b8fafd1a/divider.png