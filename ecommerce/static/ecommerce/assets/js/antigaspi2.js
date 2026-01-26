
const products = [
    { id: 1, title: "Restaurant Le Bon Goût", subtitle: "Panier AntiGaspi - Plats cuisinés", img: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=500&q=80", category: "RESTAURANTS & SNACKS", discount: "-62%", rating: 4.6, reviews: 89, time: "Aujourd'hui - 19:00 - 21:00", location: "Brazzaville - Bacongo", price: "4 500 FCFA", oldPrice: "12 000 FCFA", remaining: 3 },
    { id: 2, title: "Épicerie Bio Nature", subtitle: "Panier AntiGaspi - Fruits & Légumes", img: "https://images.unsplash.com/photo-1610832958506-aa56368176cf?auto=format&fit=crop&w=500&q=80", category: "FRUITS & LÉGUMES", discount: "-58%", rating: 4.9, reviews: 167, time: "Aujourd'hui - 18:30 - 20:00", location: "Brazzaville - Moungali", price: "2 500 FCFA", oldPrice: "6 000 FCFA", remaining: 4 },
    { id: 3, title: "SuperMarché Central", subtitle: "Panier AntiGaspi - Mix supermarché", img: "https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=500&q=80", category: "SUPERMARCHÉS & ÉPICERIES", discount: "-65%", rating: 4.7, reviews: 203, time: "Aujourd'hui - 17:30 - 19:30", location: "Pointe-Noire - Centre-ville", price: "3 500 FCFA", oldPrice: "10 000 FCFA", remaining: 8 },
    { id: 4, title: "Le Fournil d'Or", subtitle: "Panier AntiGaspi - Pains & Viennoiseries", img: "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=500&q=80", category: "BOULANGERIES & PÂTISSERIES", discount: "-64%", rating: 4.6, reviews: 134, time: "Aujourd'hui - 17:00 - 19:00", location: "Brazzaville - Centre-ville", price: "2 300 FCFA", oldPrice: "6 500 FCFA", remaining: 7 },
    { id: 5, title: "Boulangerie La berne", subtitle: "Panier AntiGaspi - Pains & Viennoiseries", img: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=500&q=80", category: "BOULANGERIES & PÂTISSERIES", discount: "-60%", rating: 4.5, reviews: 52, time: "Aujourd'hui - 17:30 - 19:30", location: "Brazzaville - Bacongo", price: "2 200 FCFA", oldPrice: "5 500 FCFA", remaining: 5 }
];

const productsGrid2 = [
    { id: 101, title: "Chez Maman Chérie", subtitle: "Panier AntiGaspi - Plats faits maison", img: "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=500&q=80", category: "RESTAURANTS & SNACKS", discount: "-55%", rating: 4.5, reviews: 45, time: "Aujourd'hui - 18:00 - 20:00", location: "Brazzaville - Ouenzé", price: "3 200 FCFA", oldPrice: "7 000 FCFA", remaining: 4 },
    { id: 102, title: "Patisserie Royale", subtitle: "Panier AntiGaspi - Pâtisseries fraîches", img: "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=500&q=80", category: "BOULANGERIES & PÂTISSERIES", discount: "-59%", rating: 4.7, reviews: 82, time: "Aujourd'hui - 17:00 - 19:00", location: "Brazzaville - Centre-ville", price: "2 800 FCFA", oldPrice: "6 800 FCFA", remaining: 6 },
    { id: 103, title: "Marché Frais du Congo", subtitle: "Panier AntiGaspi - Légumes & Fruits", img: "https://images.unsplash.com/photo-1506806732259-39c2d0268443?auto=format&fit=crop&w=500&q=80", category: "FRUITS & LÉGUMES", discount: "-60%", rating: 4.6, reviews: 60, time: "Aujourd'hui - 16:30 - 18:30", location: "Brazzaville - Bacongo", price: "2 200 FCFA", oldPrice: "5 500 FCFA", remaining: 5 },
    { id: 104, title: "Épicerie du Lac", subtitle: "Panier AntiGaspi - Épicerie", img: "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=500&q=80", category: "ÉPICERIE", discount: "-62%", rating: 4.4, reviews: 34, time: "Aujourd'hui - 19:00 - 21:00", location: "Brazzaville - Poto-Poto", price: "3 000 FCFA", oldPrice: "8 000 FCFA", remaining: 2 },
    { id: 105, title: "Traiteur du Marché", subtitle: "Plateau Traiteur - Économique", img: "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=500&q=80", category: "TRAITEUR", discount: "-59%", rating: 4.3, reviews: 28, time: "Aujourd'hui - 20:00 - 22:00", location: "Brazzaville - Talangai", price: "4 500 FCFA", oldPrice: "11 000 FCFA", remaining: 3 }
];

const nearbyProducts = [
    { id: 6, title: "Super U Express", subtitle: "Panier Produits Frais", img: "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=500&q=80", category: "SUPERMARCHÉ", discount: "-60%", rating: null, reviews: null, time: "20:00 - 21:00", location: "Centre-ville, Pointe-Noire", price: "4 000 FCFA", oldPrice: "10 000 FCFA", remaining: null },
    { id: 7, title: "Chez Tonton Grill", subtitle: "Box Grillades du Soir", img: "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=500&q=80", category: "Plus que 2 !", categoryColor: "#e67e22", discount: "-58%", rating: null, reviews: null, time: "21:00 - 22:00", location: "Quartier Lumumba, Pointe-Noire", price: "5 000 FCFA", oldPrice: "12 000 FCFA", remaining: null },
    { id: 8, title: "La Croissanterie", subtitle: "Viennoiseries du Matin", img: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=500&q=80", category: "BOULANGERIE", discount: "-67%", rating: null, reviews: null, time: "11:00 - 12:00", location: "Talangai, Brazzaville", price: "1 500 FCFA", oldPrice: "4 500 FCFA", remaining: null },
    { id: 9, title: "Saveurs d'Afrique", subtitle: "Plateau Traiteur", img: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=500&q=80", category: "Plus que 1 !", categoryColor: "#e67e22", discount: "-60%", rating: null, reviews: null, time: "18:00 - 19:00", location: "Ouenzé, Brazzaville", price: "6 000 FCFA", oldPrice: "15 000 FCFA", remaining: null }
];

// --- FONCTIONS ---
function createCard(product) {
    const hasRating = product.rating ? `
        <div class="rating">
            <i class="fas fa-star star"></i> <strong>${product.rating}/5</strong>
            <span class="rating-count">(${product.reviews} avis)</span>
        </div>` : '';
    const remainingText = product.remaining ? `<span class="items-left">${product.remaining} restants</span>` : '';
    const catStyle = product.categoryColor ? `background-color:${product.categoryColor}; color:white;` : '';

    return `
        <div class="card">
            <div class="card-image-container">
                <img src="${product.img}" alt="${product.title}" class="card-img">
                <span class="badge-cat" style="${catStyle}">${product.category}</span>
                <span class="badge-discount">${product.discount}</span>
            </div>
            <div class="card-content">
                <div class="card-title">${product.title}</div>
                <div class="card-subtitle">${product.subtitle}</div>
                ${hasRating}
                <div class="info-row"><i class="far fa-clock"></i> ${product.time}</div>
                <div class="info-row"><i class="fas fa-map-marker-alt"></i> ${product.location}</div>
                <div class="price-section">
                    <div>
                        <span class="price-new">${product.price}</span>
                        <div style="display:inline-block">
                            <span style="font-size:0.6rem; color:#999; display:block; line-height:1;">Valeur réelle</span>
                            <span class="price-old">${product.oldPrice}</span>
                        </div>
                    </div>
                    ${remainingText}
                </div>
                <button class="btn-reserve">Réserver ce panier</button>
            </div>
        </div>
    `;
}

// --- LOGIQUE DE FILTRAGE ---
function norm(s){ return (s||'').toString().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,''); }
function parsePrice(priceStr){ const n = (priceStr||'').replace(/\s/g,'').replace(/[^0-9]/g,''); return n ? parseInt(n,10) : NaN; }
function parseDiscount(str){ const n = (str||'').replace(/[^0-9\-]/g,''); return n ? Math.abs(parseInt(n,10)) : 0; }
function parseStartHour(timeStr){ if(!timeStr) return null; const m = timeStr.match(/(\d{1,2}):\d{2}/); return m ? parseInt(m[1],10) : null; }

function matchesCommerce(product, selected){
    if(!selected || selected.length===0 || selected.includes('Tous')) return true;
    const txt = norm(product.category + ' ' + product.subtitle + ' ' + product.title);
    return selected.some(c => {
        const key = norm(c);
        if(key.includes('supermarche')) return /supermarch|epic/.test(txt);
        if(key.includes('boulanger')) return /boulanger|patis/.test(txt);
        if(key.includes('restaurant')) return /restaur|snack|traiteur/.test(txt);
        if(key.includes('fruit')) return /fruit|legum/.test(txt);
        return txt.includes(key);
    });
}

function matchesPanier(product, selected){
    if(!selected || selected.length===0 || selected.includes('Tous')) return true;
    const txt = norm(product.subtitle + ' ' + product.title);
    return selected.some(p => {
        const key = norm(p);
        if(key.includes('petit')) return /petit|matin/.test(txt);
        if(key.includes('dejeuner')) return /dejeun|diner|plat/.test(txt);
        if(key.includes('mix')) return /mix|supermarch/.test(txt);
        if(key.includes('patis')) return /patis|viennois/.test(txt);
        return txt.includes(key);
    });
}

function matchesCreneau(product, val){
    if(!val || val === "") return true;
    const h = parseStartHour(product.time);
    if(h===null) return true;
    if(val.includes('Matin')) return h >= 6 && h < 11;
    if(val.includes('Midi')) return h >= 11 && h < 15;
    if(val.includes('Soir')) return h >= 15 && h < 23;
    return true;
}

function matchesBudget(product, val){
    if(val === 'all') return true;
    const p = parsePrice(product.price);
    if(isNaN(p)) return true;
    if(val === 'lt2000') return p < 2000;
    if(val === '2000-5000') return p >= 2000 && p <= 5000;
    if(val === 'gt5000') return p > 5000;
    return true;
}

function matchesReduction(product, val){
    if(val === 'all') return true;
    const d = parseDiscount(product.discount);
    return d >= parseInt(val, 10);
}

function matchesCity(product, city){
    if(!city || city === 'Toutes les villes du Congo') return true;
    return product.location.toLowerCase().includes(city.toLowerCase());
}

function getSelectedFilters(){
    const commerce = Array.from(document.querySelectorAll('#pills-group-1 .pill.active')).map(el => el.textContent.trim());
    const panier = Array.from(document.querySelectorAll('#pills-group-2 .pill.active')).map(el => el.textContent.trim());
    
    return {
        commerce: commerce,
        panier: panier,
        date: document.getElementById('filter-date').value,
        creneau: document.getElementById('filter-creneau').value,
        budget: document.getElementById('filter-budget').value,
        reduc: document.getElementById('filter-reduc').value,
        sort: document.querySelector('.sort-select').value,
        city: document.querySelector('.city-select').value
    };
}

// --- RENDERING PRINCIPAL ---
function renderAll() {
    const filters = getSelectedFilters();

    const filterFn = (p) => {
        return matchesCommerce(p, filters.commerce) &&
               matchesPanier(p, filters.panier) &&
               matchesCreneau(p, filters.creneau) &&
               matchesBudget(p, filters.budget) &&
               matchesReduction(p, filters.reduc) &&
               matchesCity(p, filters.city);
    };

    const sortFn = (a, b) => {
        if (filters.sort === 'Prix croissant') {
            return parsePrice(a.price) - parsePrice(b.price);
        } else if (filters.sort === 'Prix décroissant') {
            return parsePrice(b.price) - parsePrice(a.price);
        } else if (filters.sort === 'Les plus proches') {
            return a.location.localeCompare(b.location);
        }
      
        return 0;
    };

    const fillGrid = (id, data) => {
        let filtered = data.filter(filterFn);
        filtered.sort(sortFn);
        document.getElementById(id).innerHTML = filtered.length ? filtered.map(createCard).join('') : '<p style="grid-column:1/-1; text-align:center; color:#888;">Aucun résultat pour ces filtres.</p>';
    };

    fillGrid('product-grid', products);
    fillGrid('product-grid-2', productsGrid2);
    fillGrid('nearby-grid', nearbyProducts);
}



let currentSection = 0;
const sections = ['product-grid', 'product-grid-2', 'nearby-grid'];

function navigateSections(direction) {
    currentSection = (currentSection + direction + sections.length) % sections.length;
    const target = document.getElementById(sections[currentSection]);
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

document.querySelectorAll('.pill').forEach(pill => {
    pill.addEventListener('click', function() {
        const parent = this.parentElement;
        if(this.textContent.trim() === 'Tous') {
            parent.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
            this.classList.add('active');
        } else {
            const tousBtn = Array.from(parent.querySelectorAll('.pill')).find(p => p.textContent.trim() === 'Tous');
            if(tousBtn) tousBtn.classList.remove('active');
            this.classList.toggle('active');
            if(parent.querySelectorAll('.pill.active').length === 0 && tousBtn) {
                tousBtn.classList.add('active');
            }
        }
        renderAll();
    });
});

document.querySelectorAll('.dropdown-select').forEach(select => {
    select.addEventListener('change', renderAll);
});

document.querySelector('.sort-select').addEventListener('change', renderAll);

document.querySelector('.city-select').addEventListener('change', renderAll);

// --- GEOLOCATION ---
document.getElementById('detect-location').addEventListener('click', function() {
    if (navigator.geolocation) {
        this.innerHTML = '<i class="fas fa-map-marker-alt"></i> Détection en cours...';
        this.disabled = true;
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                reverseGeocode(lat, lon);
            },
            function(error) {
                alert('Erreur de géolocalisation: ' + error.message);
                document.getElementById('detect-location').innerHTML = '<i class="fas fa-map-marker-alt"></i> Détecter ma position';
                document.getElementById('detect-location').disabled = false;
            }
        );
    } else {
        alert('La géolocalisation n\'est pas supportée par ce navigateur.');
    }
});

function reverseGeocode(lat, lon) {
    const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10&addressdetails=1`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            let city = null;
            if (data && data.address) {
                city = data.address.city || data.address.town || data.address.village || data.address.hamlet;
            }
            if (city) {
                
                const normalizedCity = normalizeCityName(city);
                const select = document.querySelector('.city-select');
                const options = Array.from(select.options);
                const matchingOption = options.find(option => option.value.toLowerCase() === normalizedCity.toLowerCase());
                if (matchingOption) {
                    select.value = matchingOption.value;
                    renderAll();
                } else {
                    alert(`Ville détectée: ${city}. Elle n'est pas dans la liste des villes disponibles.`);
                }
            } else {
                alert('Impossible de déterminer la ville à partir de votre position.');
            }
            document.getElementById('detect-location').innerHTML = '<i class="fas fa-map-marker-alt"></i> Détecter ma position';
            document.getElementById('detect-location').disabled = false;
        })
        .catch(error => {
            alert('Erreur lors de la récupération des informations de localisation: ' + error.message);
            document.getElementById('detect-location').innerHTML = '<i class="fas fa-map-marker-alt"></i> Détecter ma position';
            document.getElementById('detect-location').disabled = false;
        });
}

function normalizeCityName(city) {
    
    const mappings = {
        'Brazzaville': 'Brazzaville',
        'Pointe-Noire': 'Pointe-Noire',
        'Dolisie': 'Dolisie',
        'Kinkala': 'Kinkala',
        'Mindouli': 'Mindouli',
        'Kindamba': 'Kindamba',
        'Nkayi': 'Nkayi',
        'Madingou': 'Madingou', 
        'Makoua': 'Makoua',
        'Impfondo': 'Impfondo',
        'Gamboma': 'Gamboma',
        'Ouesso': 'Ouesso',
        'Owando': 'Owando',
        'Oyo': 'Oyo',
        'Loango': 'Loango',
        'Mossendjo': 'Mossendjo',
        // Ajouter & retirer d'autres villes si nécessaire
    };
    return mappings[city] || city;
}


document.getElementById('reset-filters').addEventListener('click', function(){
    // 1. Enlever 'active' de partout
    document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
    
    // 2. Remettre 'active' UNIQUEMENT sur les boutons qui s'appellent "Tous"
    document.querySelectorAll('.pill').forEach(p => {
        if(p.textContent.trim() === "Tous") {
            p.classList.add('active');
        }
    });

    // 3. Reset selects
    document.getElementById('filter-date').value = "";
    document.getElementById('filter-creneau').value = "";
    document.getElementById('filter-budget').value = "all";
    document.getElementById('filter-reduc').value = "all";
    
    renderAll();
});

document.getElementById('nav-prev').addEventListener('click', () => navigateSections(-1));
document.getElementById('nav-next').addEventListener('click', () => navigateSections(1));

renderAll();

// Footer year (copié depuis Antigaspi1)
const yearSpan = document.getElementById('year-footer');
if (yearSpan) yearSpan.textContent = new Date().getFullYear();
