document.addEventListener('DOMContentLoaded', () => {
    // 1. Récupération de l'état utilisateur et du token CSRF
    // Ces variables doivent être définies globalement dans base.html ou lues depuis des meta tags
    const isAuthenticated = (window.USER_IS_AUTHENTICATED === true);
    const csrfToken = window.CSRF_TOKEN || '';

    // 2. Gestion du LocalStorage pour les favoris (visiteurs non connectés)
    const getLocalFavorites = () => {
        try {
            return JSON.parse(localStorage.getItem('oyeo_favorites') || '[]');
        } catch (e) { return []; }
    };

    const setLocalFavorites = (favs) => {
        localStorage.setItem('oyeo_favorites', JSON.stringify(favs));
    };

    const isLocalFavorite = (id) => getLocalFavorites().includes(id.toString());

    const toggleLocalFavorite = (id) => {
        let favs = getLocalFavorites();
        const strId = id.toString();
        const index = favs.indexOf(strId);
        let added = false;

        if (index === -1) {
            favs.push(strId);
            added = true;
        } else {
            favs.splice(index, 1);
            added = false;
        }
        setLocalFavorites(favs);
        return added;
    };

    // 3. Mise à jour de l'UI au chargement (pour les anonymes surtout)
    // Si l'utilisateur est connecté, le serveur a déjà rendu l'état initial correct via le template.
    // Si l'utilisateur n'est PAS connecté, on doit appliquer l'état depuis le localStorage.
    if (!isAuthenticated) {
        document.querySelectorAll('.fav-icon').forEach(icon => {
            const productId = icon.dataset.productId;
            if (productId && isLocalFavorite(productId)) {
                icon.classList.add('favorited');
            }
        });
        // Update header count for anonymous
        updateHeaderFavoriteCount(getLocalFavorites().length);
    } else {
        // Authenticated users: initial count should be injected or fetched.
        // If passed via window.USER_FAVORITES_COUNT, use it, otherwise fetch or count based on DOM (less reliable if pagination)
        // For simplicity, let's assume we can rely on a global variable or fetch it if needed.
        if (typeof window.USER_FAVORITES_COUNT !== 'undefined') {
             updateHeaderFavoriteCount(window.USER_FAVORITES_COUNT);
        } else {
            // Fallback: If not provided, we might show nothing or fetch it.
            // Let's rely on the template injection in base.html for the initial count.
        }
    }

    // Fonction pour mettre à jour le badge dans le header
    function updateHeaderFavoriteCount(count) {
        const badge = document.getElementById('fav-count-badge');
        if (!badge) return;

        if (count > 0) {
            badge.textContent = count;
            badge.style.display = 'inline-block';
        } else {
            badge.style.display = 'none';
        }
    }

    // 4. Gestion du clic sur l'icône
    document.body.addEventListener('click', async (e) => {
        // Délégation d'événement pour gérer les éléments chargés dynamiquement
        const icon = e.target.closest('.fav-icon');
        if (!icon) return;

        e.preventDefault();
        e.stopPropagation(); // Empêcher d'ouvrir la fiche produit au clic sur le cœur

        const productId = icon.dataset.productId;
        if (!productId) return;

        // --- Cas Utilisateur Connecté ---
        if (isAuthenticated) {
            try {
                const response = await fetch('/ajax/toggle-favorite/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ product_id: productId })
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.favorited) {
                        updateIconState(productId, true);
                        showNotification("Ajouté aux favoris", "success");
                    } else {
                        updateIconState(productId, false);
                        showNotification("Retiré des favoris", "info");
                    }
                    // Update count from server response
                    updateHeaderFavoriteCount(data.count);
                } else {
                    console.error('Erreur serveur toggle favori');
                    showNotification("Erreur lors de la mise à jour", "error");
                }
            } catch (err) {
                console.error('Erreur réseau:', err);
                showNotification("Erreur de connexion", "error");
            }
        } 
        // --- Cas Utilisateur Non Connecté (LocalStorage) ---
        else {
            const added = toggleLocalFavorite(productId);
            updateIconState(productId, added);
            if (added) {
                // showNotification("Ajouté aux favoris (local)", "success");
            } else {
                // showNotification("Retiré des favoris (local)", "info");
            }
            // Update count from local storage
            updateHeaderFavoriteCount(getLocalFavorites().length);
        }
    });


    // Fonction pour mettre à jour TOUTES les occurrences de l'icône pour ce produit sur la page
    function updateIconState(productId, isFavorited) {
        document.querySelectorAll(`.fav-icon[data-product-id="${productId}"]`).forEach(el => {
            if (isFavorited) {
                el.classList.add('favorited');
            } else {
                el.classList.remove('favorited');
            }
        });
    }

    // 5. Système de Notification (Toast simple)
    function showNotification(message, type = 'success') {
        let container = document.getElementById('fav-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'fav-toast-container';
            container.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 10000;
                display: flex;
                flex-direction: column;
                gap: 10px;
            `;
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        // Couleurs selon le type
        const bgColor = type === 'error' ? '#e74c3c' : (type === 'info' ? '#34495e' : '#2ecc71');
        
        toast.style.cssText = `
            background-color: ${bgColor};
            color: #fff;
            padding: 12px 24px;
            border-radius: 4px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            font-family: 'Quicksand', sans-serif;
            font-size: 14px;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
            min-width: 200px;
            text-align: center;
        `;
        toast.textContent = message;

        container.appendChild(toast);

        // Animation d'entrée
        requestAnimationFrame(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
        });

        // Suppression automatique
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            setTimeout(() => {
                if (toast.parentElement) toast.parentElement.removeChild(toast);
            }, 300);
        }, 3000);
    }
});
