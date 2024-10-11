
let phoneNumber = NaN;
let error_404 = NaN;

function clickshowButton() {

    // Wait for the first listing to load
    // waitForElm('.tracking-root').then((elm) => {
    //     console.log('Element is ready');
    // });

    // click show button
    main_element = document.querySelector('.tracking-root');
    show_button = main_element.querySelector('[data-component="Link"]').click();
}

function scrape_and_export_number(){
    main_element = document.querySelector('.tracking-root');
    try{
        phoneNumber = main_element.querySelector('a[data-component="Link"]').innerText;
    }
    catch(error){
        console.log('Phone number not found.');
    }
    
    if (phoneNumber) {
        console.log(`Phone Number: ${phoneNumber}`);
        exportValueToTextFile(phoneNumber, 'agent_number.txt');
    }
    else {
        error_404 = document.querySelector("#appContent > section > div > h2").innerText;
        exportValueToTextFile(error_404, 'agent_number.txt');
    }
}

function exportValueToTextFile(value, fileName) {
    // Create a blob with the text content and specify the MIME type as plain text
    const blob = new Blob([value], { type: 'text/plain' });

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


// function waitForElm(selector) {
//     return new Promise(resolve => {
//         if (document.querySelector(selector)) {
//             return resolve(document.querySelector(selector));
//         }

//         const observer = new MutationObserver(mutations => {
//             if (document.querySelector(selector)) {
//                 observer.disconnect();
//                 resolve(document.querySelector(selector));
//             }
//         });

//         observer.observe(document.body, {
//             childList: true,
//             subtree: true
//         });
//     });
// }
