let = pages = [];

function startScraping() {
    // Wait for the first listing to load
    waitForElm('.tracking-root').then((elm) => {
        console.log('Element is ready');
    });
    const listings = document.querySelectorAll('.tracking-root');
    let counter = 1; 

    for (const listing of listings) {
        // Stop the loop after 36 iterations
        if (counter >= 36) {
            break;
        }

        // Scrape the URL and property name
        const anchor = listing.querySelector('a[data-cy="listingName"]');
        const url = anchor.href;
        pages.push(url);

        counter++;
    }
    console.log(`Pages Scraped: ${counter}`)
    exportListToTextFile(pages, 'property_urls.txt');
}

function exportListToTextFile(list, fileName) {
    // Join the list into a single string, with each item on a new line
    const content = list.join('\n');

    // Create a blob with the text content and specify the MIME type as plain text
    const blob = new Blob([content], { type: 'text/plain' });

    // Create a temporary link element
    const link = document.createElement('a');

    // Set the download URL to the blob
    link.href = URL.createObjectURL(blob);

    // Set the download attribute with the desired file name
    link.download = fileName;

    // Programmatically click the link to trigger the download
    link.click();

    // Clean up by revoking the object URL
    URL.revokeObjectURL(link.href);
}

function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                observer.disconnect();
                resolve(document.querySelector(selector));
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}
