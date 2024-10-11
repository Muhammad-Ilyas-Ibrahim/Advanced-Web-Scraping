var data = [];

function getAgentContact() {
    let phoneNumber = 'N/A';
    const phoneElement = document.querySelector('a[href^="tel:"]');

    if (phoneElement) {
        phoneNumber = phoneElement.textContent.trim();
        phoneNumber = phoneNumber.replace(/\s/g, '');
    } else {
        console.log("Phone number not found.");
    }
    return phoneNumber  
}

function extractData() {

    let pageURL = window.location.href;
    let propertyName = 'N/A';
    let agentName = 'N/A';
    let agentContact = 'N/A';
    let agentProfile = 'N/A';


    // Extract Property Name
    // Find the h element with the class containing "Heading_heading1"
    const h_e = document.querySelector('[class*="Heading_heading1"]');

    if (h_e) {
        const a_tags = h_e.querySelectorAll('a');

        if (a_tags.length > 0) {
            const last_a_tag = a_tags[a_tags.length - 1];

            propertyName = last_a_tag.innerText;
        } else {
            console.log('<a> tags not found within the specified element.');
        }
    } else {
        console.log('Element with class containing "Heading_heading1" not found.');
    }

    // Scrape Agent name
    agentName = document.querySelector('[class*="EnquiryForm_agentName"]').innerText;

    // Find and Go to Agent Profile
    const agentInfoElement = document.querySelector('[class*="EnquiryForm_agentInfo"]');

    // Check if the element exists
    if (agentInfoElement) {
        // Find the first <a> tag within the element
        const firstAnchorTag = agentInfoElement.querySelector('a');

        // Check if the <a> tag exists
        if (firstAnchorTag) {
            // Get the href attribute from the <a> tag
            const href = firstAnchorTag.getAttribute('href');
            if (href) {
                agentProfile = new URL(href, window.location.origin).href;
            } else {
            // Construct the full URL (if necessary, prepend the base URL)
            agentProfile = null;
            }
        } else {
            console.log('<a> tag not found within the specified element.');
        }
    } else {
        console.log('Element with class containing "EnquiryForm_agentInfo" not found.');
    }

    // extract phone number
    agentContact = getAgentContact();

    console.log(`Page URL: ${pageURL}`);
    console.log(`Property Name: ${propertyName}`);
    console.log(`Agent Name: ${agentName}`);
    console.log(`Agent Contact: ${agentContact}`);
    console.log(`Agent Profile: ${agentProfile}`);

    data.push({
        pageURL,
        propertyName,
        agentName,
        agentContact,
        agentProfile,
    });

}

function exportData() {
    const jsonData = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });

    // Create a link to download the file
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'property_data.json';

    // Automatically click the link to trigger the download
    link.click();
}

function clickShowButton() {
    const showButton = document.querySelector('span[data-cy="show"]');

    // Check if the button exists, then click it
    if (showButton) {
        showButton.click();
    } else {
        console.log('Show button not found.');
    }
}