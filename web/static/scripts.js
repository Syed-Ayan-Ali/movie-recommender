let currentPage = 1;
let totalItems = 0;
const itemsPerPage = 10;

async function fetchCategories() {
    const response = await fetch('/categories');
    const categories = await response.json();
    console.log("Categories received:", categories);

    populateFilters('genres', categories.genres);
    populateYears('years', categories.years);
}

function populateFilters(filterId, items) {
    const container = document.getElementById(filterId);
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

function populateYears(filterId, items) {
    const container = document.getElementById(filterId);
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

async function filterMovies(page) {
    const genres = getCheckedValues('genres');
    const cast = document.getElementById('cast').value.trim().toLowerCase();
    const title = document.getElementById('title').value.trim().toLowerCase();
    const years = getCheckedValues('years');
    const description = document.getElementById('description').value.trim().toLowerCase();
    const filter_logic = document.querySelector('input[name="filter_logic"]:checked').value;
    const mood = document.getElementById('mood').value.trim().toLowerCase();

    const filters = { genres: genres, cast: cast, title: title, years: years, description: description, filter_logic: filter_logic, mood: mood, page: page, items_per_page: itemsPerPage };
    console.log('Filters:', filters);
    try {
        const response = await fetch('/movies', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });

        const result = await response.json();
        totalItems = result.total_items;
        currentPage = result.page;
        displayMovies(result.movies);
        updatePagination();
    } catch (error) {
        console.error('Error:', error);
    }
}

function getCheckedValues(filterId) {
    const checkboxes = document.querySelectorAll(`#${filterId} input[type="checkbox"]:checked`);
    return Array.from(checkboxes).map(checkbox => checkbox.value);
}

function displayMovies(movies) {
    const container = document.getElementById('movies');
    container.innerHTML = '';
    movies.forEach(movie => {
        const movieDiv = document.createElement('div');
        movieDiv.innerHTML = `
            <a href="${movie.link}" target="_blank">${movie.title} (${movie.year})</a>
            <p>Genres: ${movie.genres}</p>
            <p>Cast: ${movie.cast}</p>
            <p>${movie.description}</p>
        `;
        container.appendChild(movieDiv);
    });
}

function updatePagination() {
    const paginationList = document.getElementById('pagination-list');
    paginationList.innerHTML = '';

    const totalPages = Math.ceil(totalItems / itemsPerPage);
    if (totalPages <= 1) return;

    // Add "First" button
    const firstPageItem = document.createElement('li');
    firstPageItem.className = 'page-item';
    firstPageItem.innerHTML = `<a class="page-link nav-button" href="#" onclick="filterMovies(1)">&#171;</a>`;
    paginationList.appendChild(firstPageItem);

    // Add "Previous" button
    if (currentPage > 1) {
        const prevPageItem = document.createElement('li');
        prevPageItem.className = 'page-item';
        prevPageItem.innerHTML = `<a class="page-link nav-button" href="#" onclick="filterMovies(${currentPage - 1})">&#8249;</a>`;
        paginationList.appendChild(prevPageItem);
    }

    // Add page number buttons
    let startPage = Math.max(1, currentPage - 1);
    let endPage = Math.min(totalPages, currentPage + 1);

    if (startPage > 1) {
        const firstPage = document.createElement('li');
        firstPage.className = 'page-item';
        firstPage.innerHTML = `<a class="page-link" href="#" onclick="filterMovies(1)">1</a>`;
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
        pageItem.innerHTML = `<a class="page-link" href="#" onclick="filterMovies(${i})">${i}</a>`;
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
        lastPage.innerHTML = `<a class="page-link" href="#" onclick="filterMovies(${totalPages})">${totalPages}</a>`;
        paginationList.appendChild(lastPage);
    }

    // Add "Next" button
    if (currentPage < totalPages) {
        const nextPageItem = document.createElement('li');
        nextPageItem.className = 'page-item';
        nextPageItem.innerHTML = `<a class="page-link nav-button" href="#" onclick="filterMovies(${currentPage + 1})">&#8250;</a>`;
        paginationList.appendChild(nextPageItem);
    }

    // Add "Last" button
    const lastPageItem = document.createElement('li');
    lastPageItem.className = 'page-item';
    lastPageItem.innerHTML = `<a class="page-link nav-button" href="#" onclick="filterMovies(${totalPages})">&#187;</a>`;
    paginationList.appendChild(lastPageItem);
}

window.onload = fetchCategories;
