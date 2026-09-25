<p align="center">
<img width="300" src="https://i.imgur.com/puyIfHT.jpg" /><br>
A Web Dashboard for Nmap XML reports
</p>

![WebMap](https://i.imgur.com/U9S089v.png)

![WebMap](https://i.imgur.com/Ptijc67.png)

![WebMap](https://i.imgur.com/alWZix9.png)

## Table Of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Technology Stack](#technology-stack)
- [SETUP Instructions](#setup-instructions)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
- [Video](#video)
- [Features](#features)
- [XML Filenames](#xml-filenames)
- [Third Parts](#third-parts)
- [Security Issues](#security-issues)
- [Contributors](#contributors)
- [Contacts](#contacts)

## Project Overview
WebMap is a Django-based web UI for Nmap XML output.
It lets you load scans from disk, browse hosts and ports, annotate findings (labels + notes), inspect script output, and export a PDF report.

## Repository Structure
This repository is a Django app module (not a full Django project scaffold by itself).

- `/home/runner/work/webmap/webmap/views.py`  
  Main HTML view logic for scan list, scan dashboard, host details, filters, counters, and charts.
- `/home/runner/work/webmap/webmap/api.py`  
  AJAX endpoints for labels, notes, port details, and PDF generation.
- `/home/runner/work/webmap/webmap/pdf.py`  
  Builds the HTML used by wkhtmltopdf for report export.
- `/home/runner/work/webmap/webmap/templates/nmapreport/`  
  Django templates (`index.html`, `report.html`).
- `/home/runner/work/webmap/webmap/static/`  
  Frontend assets (CSS, JavaScript, logos).
- `/home/runner/work/webmap/webmap/functions.py`  
  Small mapping helpers (labels/colors/icons).
- `/home/runner/work/webmap/webmap/urls.py`  
  URL routing for pages and API.

## Technology Stack
- Python + Django
- xmltodict for Nmap XML parsing
- Materialize CSS + jQuery for UI
- Chart.js + Google Charts for data visualization
- Clipboard.js for copy-to-clipboard actions
- wkhtmltopdf for PDF export

## SETUP Instructions
Use Docker to run WebMap quickly.

### 1) Create a local folder for scan XML files
```bash
mkdir -p /tmp/webmap
```

### 2) Start the WebMap container
```bash
docker run -d \
  --name webmap \
  -h webmap \
  -p 8000:8000 \
  -v /tmp/webmap:/opt/xml \
  rev3rse/webmap /run.sh
```

### 3) Generate and save an Nmap XML report
```bash
nmap -sT -A -T4 -oX /tmp/webmap/myscan.xml 192.168.1.0/24
```

### 4) Open the UI
Go to: `http://localhost:8000`

### 5) Use the tool
1. Select your scan file from the scan list.
2. Review discovered hosts/ports and charts.
3. Click hosts for detailed service/port information.
4. Add labels and notes where needed.
5. Generate the PDF report from the floating action button.

## Usage
### Docker (recommended)
```bash
$ mkdir /tmp/webmap
$ docker run -d \
         --name webmap \
         -h webmap \
         -p 8000:8000 \
         -v /tmp/webmap:/opt/xml \
         rev3rse/webmap /run.sh

$ # now you can run Nmap and save the XML Report on /tmp/webmap
$ nmap -sT -A -T4 -oX /tmp/webmap/myscan.xml 192.168.1.0/24
```
Now point your browser to http://localhost:8000

### Typical workflow
1. Place one or more `.xml` Nmap reports in the mounted XML directory (`/opt/xml` in the container).
2. Open WebMap and pick a scan file from the scan list.
3. Review host table, port states, top services, and charts.
4. Click a host IP to open host-level details.
5. Add host labels (`Vulnerable`, `Critical`, `Warning`, `Checked`) and notes.
6. Use port detail actions to inspect scripts or copy commands (curl/nikto/telnet).
7. Generate a PDF report from the floating action button.

### Data directories used by the app
- XML input: `/opt/xml`
- Labels/notes storage: `/opt/notes`
- Generated PDF output: `/opt/nmapdashboard/nmapreport/static`

## How It Works
1. XML is parsed server-side with `xmltodict`.
2. Parsed data is transformed into HTML fragments in Django views.
3. Frontend JavaScript calls API endpoints for labels/notes/port details/PDF.
4. Notes and labels are persisted as files under `/opt/notes`.
5. PDF export renders `/view/pdf/` with session cookie and converts it via wkhtmltopdf.

## API Endpoints
- `GET /report/api/setlabel/<objtype>/<label>/<hashstr>/`  
  Set a host/port label.
- `GET /report/api/rmlabel/<objtype>/<hashstr>/`  
  Remove a host/port label.
- `POST /report/api/savenotes/`  
  Save host notes.
- `GET /report/api/rmnotes/<hashstr>/`  
  Remove host notes.
- `GET /report/api/<address>/<portid>/`  
  Get raw details for a specific port on a host.
- `GET /report/api/pdf/`  
  Trigger PDF report generation.

## Video
-- coming soon...

## Features
- Import and parse Nmap XML files
- Statistics and Charts on discovered services, ports, OS, etc...
- Inspect a single host by clicking on its IP address
- Attach labels on a host
- Insert notes for a specific host
- Create a PDF Report with charts, details, labels and notes
- Copy to clipboard as Nikto, Curl or Telnet commands

## XML Filenames
When creating the PDF version of the Nmap XML Report, the XML filename is used as document title on the first page. WebMap will replace some parts of the filename as following:

- `_` will replaced by a space (` `)
- `.xml` will be removed

Example: `ACME_Ltd..xml`<br>
PDF title: `ACME Ltd.`

## Third Parts
- [Django](https://www.djangoproject.com)
- [Materialize CSS](https://materializecss.com)
- [Clipboard.js](https://clipboardjs.com)
- [Chart.js](https://www.chartjs.org)
- [Wkhtmltopdf](https://wkhtmltopdf.org)

## Security Issues
This app is not intended to be exposed on the internet. Please, **DO NOT expose** this app to the internet, use your localhost or, in case you can't do it, take care to filter who and what can access to WebMap with a firewall rule or something like that. Exposing this app to the whole internet could lead not only to a stored XSS but also to a leakage of sensitive/critical/private informations about your port scan. Please, be smart.

## Contributors
This project is currently a beta, and I'm not super skilled on Django so, every type of contribution is appreciated. I'll mention all contributors in this section of the README file.

### Contributors List
- s3th_0x [@adubaldo](https://github.com/adubaldo) (bug on single host report)

## Contacts
Twitter: [@Menin_TheMiddle](https://twitter.com/Menin_TheMiddle)<br>
YouTube: [Rev3rseSecurity](https://www.youtube.com/rev3rsesecurity)
