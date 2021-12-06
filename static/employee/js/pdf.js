let pdfDoc = null,
    pageNum = 1,
    pageIsRendering = false,
    pageNumIsPending = null;

const scale = 1.5;

// Render the pages
function renderPage(num, id) {
    pageIsRendering = true;
    const slide = document.querySelector(`#${id}`);

    // Get the page
    pdfDoc.getPage(num)
    .then(page => {
        slide.querySelector('.slide-loader').classList.add('hidden');
        // Set Canvas
        const canvas = document.createElement('canvas'),
            context = canvas.getContext('2d');
        canvas.id = canvas.className = `the-canvas_${num}`;
        slide.appendChild(canvas);

        // Set scale
        const viewport = page.getViewport({scale});
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        const renderContext = {
            canvasContext: context,
            viewport: viewport
        }

        page.render(renderContext)
        .promise
        .then(() => {
            pageIsRendering = false;

            if(pageNumIsPending !== null){
                renderPage(pageNumIsPending);
                pageNumIsPending = null;
            }
        });
    })
}

function renderPDF(id) {
    const slide = document.querySelector(`#${id}`);
    const URL = slide.dataset.url;

    if(URL){
        pdfjsLib.getDocument(URL)
        .promise
        .then(pdfDoc_ => {
            pdfDoc = pdfDoc_;
            for(pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++){
                renderPage(pageNum, id);
            }
        });
    }
}