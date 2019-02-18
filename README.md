# AutoBib: a quick and dirty hack to keep your publications up to date

Like most academics I struggled with keeping my personal homepage, my group
homepage, and my BIB file up to date with all the papers we publish. Instead of
allowing the individual pages go vastly out of date, I created this quick and
ugly hack to create bib files and static html pages for all different targets.

## Initial setup

* All the magic is in the poorly documented `genpubs.py`.
* Create a folder `files/` with all PDFs in it (named YYVenue.pdf, e.g.,  18CCS.pdf)
* Create a `publications.xml` with all your publications in it (follow the somewhat documented `example.xml`)
* Create a `template.html` that fits your homepage(s).

## Adding a publication
* Place the PDF in the `files/` folder.
* Update the `publications.xml` with the new publication.
* Create a bib file: `./genpubs.py -T bib -p publications.xml -o publications.bib`
* Create a html file: `./genpubs.py -t hexhive.html -p publications.xml -o ~/repos/hexhive/publications/index.html`
* Locally, I do run all these commands as part of scripts that pull the
  homepages, generate new html files, and rsync the different directories/files
  to make sure all is updated.

## Q&A
* Why? Yes, it's somewhat over-engineered but I've been using these scripts
  since 2014 years and after the initial coding they have saved me a lot of
  time.

## Author

[Mathias Payer](mailto:mathias.payer@nebelwelt.net)

Dual-licensed under the GPL and the whatever license: if it breaks, you got to
keep the pieces.  If it is helpful to you, buy me a beer the next time we meet.
