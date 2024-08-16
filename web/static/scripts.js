let currentPage = 1;
let totalItems = 0;
const itemsPerPage = 10;
let contentType = 'movies'; // Default to movies

// Function to fetch categories based on the content type (movies, series, or both)
async function fetchCategories() {
    contentType = document.querySelector('input[name="content_type"]:checked').value;
    toggleYearFilter(contentType);  // Show/hide year filter based on content type
    const response = await fetch(`/categories?type=${contentType}`);
    const categories = await response.json();
    console.log("Categories received:", categories);

    populateFilters('genres', categories.genres);
    if (contentType !== 'series') {
        populateYears('years', categories.years);
    }
}

// Function to toggle the visibility of the year filter based on content type
function toggleYearFilter(contentType) {
    const yearFilterSection = document.getElementById('year-filter');
    if (contentType === 'series') {
        yearFilterSection.style.display = 'none';  // Hide year filter if TV series is selected
    } else {
        yearFilterSection.style.display = 'block';  // Show year filter otherwise
    }
}

// Function to dynamically populate filter options
function populateFilters(filterId, items) {
    const container = document.getElementById(filterId);
    container.innerHTML = ''; // Clear previous filters
    items.forEach(item => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = item.trim();
        checkbox.id = `${filterId}-${item.trim()}`;

        const label = document.createElement('label');
        label.htmlFor = checkbox.id;
        label.textContent = item.trim();

        container.appendChild(checkbox);
        container.appendChild(label);
    });
}

// Function to populate year filters
function populateYears(filterId, items) {
    const container = document.getElementById(filterId);
    container.innerHTML = ''; // Clear previous filters
    items.forEach(item => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = item;
        checkbox.id = `${filterId}-${item}`;

        const label = document.createElement('label');
        label.htmlFor = checkbox.id;
        label.textContent = item;

        container.appendChild(checkbox);
        container.appendChild(label);
    });
}

// Function to filter content (movies or series)
async function filterContent(page) {
    const contentType = document.querySelector('input[name="content_type"]:checked').value;  // Get the content type selection
    const genres = getCheckedValues('genres');
    const cast = document.getElementById('cast').value.trim().toLowerCase();
    const title = document.getElementById('title').value.trim().toLowerCase();
    const years = getCheckedValues('years');
    const description = document.getElementById('description').value.trim().toLowerCase();
    const filter_logic = document.querySelector('input[name="filter_logic"]:checked').value;
    const mood = document.getElementById('mood').value.trim().toLowerCase();

    const filters = { 
        genres: genres, 
        cast: cast, 
        title: title, 
        years: contentType !== 'series' ? years : [],  // Only include years if it's not TV series
        description: description, 
        filter_logic: filter_logic, 
        mood: mood, 
        page: page, 
        items_per_page: itemsPerPage, 
        type: contentType  // Include the content type in the filters
    };
    console.log('Filters:', filters);

    try {
        const response = await fetch(`/content`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });

        const result = await response.json();
        totalItems = result.total_items;
        currentPage = result.page;
        displayContent(result.content);  // Display content instead of just movies
        updatePagination();
    } catch (error) {
        console.error('Error:', error);
    }
}

function getCheckedValues(filterId) {
    const checkboxes = document.querySelectorAll(`#${filterId} input[type="checkbox"]:checked`);
    return Array.from(checkboxes).map(checkbox => checkbox.value);
}

function displayContent(content) {
    const container = document.getElementById('movies'); // This can be used for both movies and series
    container.innerHTML = '';
    content.forEach(item => {
        const contentDiv = document.createElement('div');
        contentDiv.innerHTML = `
            <a href="${item.link}" target="_blank">${item.title} (${item.year || 'N/A'})</a>
            <p>Genres: ${item.genres}</p>
            <p>Cast: ${item.cast}</p>
            <p>${item.description}</p>
        `;
        container.appendChild(contentDiv);
    });
}

function updatePagination() {
    const paginationList = document.getElementById('pagination-list');
    paginationList.innerHTML = '';

    const totalPages = Math.ceil(totalItems / itemsPerPage);
    if (totalPages <= 1) return;

    const firstPageItem = document.createElement('li');
    firstPageItem.className = 'page-item';
    firstPageItem.innerHTML = `<a class="page-link nav-button" href="#" onclick="filterContent(1)">&#171;</a>`;
    paginationList.appendChild(firstPageItem);

    if (currentPage > 1) {
        const prevPageItem = document.createElement('li');
        prevPageItem.className = 'page-item';
        prevPageItem.innerHTML = `<a class="page-link nav-button" href="#" onclick="filterContent(${currentPage - 1})">&#8249;</a>`;
        paginationList.appendChild(prevPageItem);
    }

    let startPage = Math.max(1, currentPage - 1);
    let endPage = Math.min(totalPages, currentPage + 1);

    if (startPage > 1) {
        const firstPage = document.createElement('li');
        firstPage.className = 'page-item';
        firstPage.innerHTML = `<a class="page-link" href="#" onclick="filterContent(1)">1</a>`;
        paginationList.appendChild(firstPage);

        if (startPage > 2) {
            const dots = document.createElement('li');
            dots.className = 'page-item';
            dots.innerHTML = `<span class="page-link">...</span>`;
            paginationList.appendChild(dots);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        const pageItem = document.createElement('li');
        pageItem.className = 'page-item';
        if (i === currentPage) pageItem.classList.add('active');
        pageItem.innerHTML = `<a class="page-link" href="#" onclick="filterContent(${i})">${i}</a>`;
        paginationList.appendChild(pageItem);
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            const dots = document.createElement('li');
            dots.className = 'page-item';
            dots.innerHTML = `<span class="page-link">...</span>`;
            paginationList.appendChild(dots);
        }

        const lastPage = document.createElement('li');
        lastPage.className = 'page-item';
        lastPage.innerHTML = `<a class="page-link" href="#" onclick="filterContent(${totalPages})">${totalPages}</a>`;
        paginationList.appendChild(lastPage);
    }

    if (currentPage < totalPages) {
        const nextPageItem = document.createElement('li');
        nextPageItem.className = 'page-item';
        nextPageItem.innerHTML = `<a class="page-link nav-button" href="#" onclick="filterContent(${currentPage + 1})">&#8250;</a>`;
        paginationList.appendChild(nextPageItem);
    }

    const lastPageItem = document.createElement('li');
    lastPageItem.className = 'page-item';
    lastPageItem.innerHTML = `<a class="page-link nav-button" href="#" onclick="filterContent(${totalPages})">&#187;</a>`;
    paginationList.appendChild(lastPageItem);
}

document.querySelectorAll('input[name="content_type"]').forEach(radio => {
    radio.addEventListener('change', fetchCategories); // Fetch categories when content type changes
});

window.onload = function() {
    fetchCategories();
};
