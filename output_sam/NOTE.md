The sample reports' assets/ directories (fonts, MathJax, Paged.js — ~8 MB each) are omitted from the repo to keep installs light.
To re-render a sample report.html: cp -r ../../assets <sample-dir>/assets && node ../../scripts/render_pdf.mjs <sample-dir>/report.html out.pdf
