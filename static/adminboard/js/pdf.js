const slides = document.querySelectorAll('.slide');

let pdfDoc = null,
    pageNum = 1,
    pageIsRendering = false,
    pageNumIsPending = null;

const scale = 1.5;

// Render the pages
const renderPage = (num, i) => {
    pageIsRendering = true;
    
    // Get the page
    pdfDoc.getPage(num)
    .then(page => {
        // Set Canvas
        const canvas = document.createElement('canvas'),
              context = canvas.getContext('2d');
        canvas.id = canvas.className = `the-canvas`;
        slides[i].appendChild(canvas);

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

slides.forEach((slide, i) => {
    const url = slide.dataset.url;
    if(url){
        pdfjsLib.getDocument(url)
        .promise
        .then(pdfDoc_ => {
            pdfDoc = pdfDoc_;
            for(pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++){
                renderPage(pageNum, i);
            }
        })
        .catch(err => {
            // Display Error
            const div = document.createElement('div'),
                  p = document.createElement('p');
            div.className = 'error uk-flex uk-flex-middle uk-flex-center uk-padding-small background-danger';
            p.textContent = err.message;
            p.className = 'uk-margin-remove';
            div.appendChild(p);
            document.querySelector('.viewer').insertBefore(div, slide);
        })
        
    }
});