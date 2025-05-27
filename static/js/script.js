document.addEventListener('DOMContentLoaded', function () {
  // 🔒 Utility per ottenere il token CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // ❤️ Like Button
  document.querySelectorAll('.like_button').forEach(button => {
    button.addEventListener('click', function () {
      const postId = this.dataset.postId;
      const icon = this.querySelector('i');

      fetch(`/like/${postId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      }).then(response => {
        if (response.ok) {
          icon.classList.toggle('fa-solid');
          icon.classList.toggle('fa-regular');
          icon.style.color = icon.classList.contains('fa-solid') ? '#cd1818' : 'black';
        }
      });
    });
  });

  // ⭐ Wishlist Button
  document.querySelectorAll('.wishlist_button').forEach(button => {
    button.addEventListener('click', function () {
      const postId = this.dataset.postId;
      const icon = this.querySelector('i');

      fetch(`/wishlist/${postId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      }).then(response => {
        if (response.ok) {
          icon.classList.toggle('fa-solid');
          icon.classList.toggle('fa-regular');
          icon.style.color = icon.classList.contains('fa-solid') ? 'rgb(255, 217, 0)' : 'black';
        }
      });
    });
  });

  // 🎚️ Toggle filtri (Index)
  const btnFiltri = document.querySelector('.estendi-filtri');
  const layoutFiltri = document.querySelector('.layout-filtri');
  if (btnFiltri && layoutFiltri) {
    btnFiltri.addEventListener('click', function () {
      layoutFiltri.classList.toggle('show');
    });
  }

  document.addEventListener('click', function (e) {
    if (e.target.matches('.follow-button, .unfollow-button, .follow-button-2, .unfollow-button-2, .follow-toggle')) {
      const button = e.target;
      const userId = button.dataset.userId;

      fetch(`/follow/${userId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      })
        .then(response => response.json())
        .then(data => {
          // Cambia classe e testo
          const isUnfollow = button.classList.contains('unfollow-button') || button.classList.contains('unfollow-button-2');

          button.classList.toggle('follow-button', isUnfollow);
          button.classList.toggle('unfollow-button', !isUnfollow);
          button.classList.toggle('follow-button-2', isUnfollow);
          button.classList.toggle('unfollow-button-2', !isUnfollow);

          button.textContent = isUnfollow ? 'Follow' : 'Unfollow';

          // Usa user_id restituito per decidere cosa aggiornare
          const currentProfileId = document.querySelector('.profile-info').dataset.profileUserId;
          // Nel template imposta <body data-profile-user-id="{{ profile_owner.id }}"> (o equivalente)
          
          if (String(data.user_id) === currentProfileId) {
            // Sto guardando il profilo della persona seguita => aggiorno i follower
            const followerCounter = document.getElementById('follower-count');
            if (followerCounter) {
              followerCounter.textContent = data.follower_count;
            }
          } else if (String(userId) === currentProfileId) {
            // Se sto sul mio profilo, e sto modificando i miei seguiti
            // Aggiorno i seguiti
            const seguitiCounter = document.getElementById('seguiti-count');
            if (seguitiCounter) {
              seguitiCounter.textContent = data.seguiti_count;
            }
          } else {
            // Se sei in qualche altra pagina (es. lista seguiti), aggiorna seguiti count
            const seguitiCounter = document.getElementById('seguiti-count');
            if (seguitiCounter) {
              seguitiCounter.textContent = data.seguiti_count;
            }
          }
        });
    }
  });
});

// 🔄 Funzione globale per resettare i filtri
function resetFiltri() {
  document.getElementById('titolo').value = '';
  document.getElementById('proprietario').value = '';
  document.getElementById('condizioni').value = '';
  document.getElementById('ordinamento').value = 'data_desc';
  document.getElementById('filterForm').submit();
}

document.getElementById('ordinamento').addEventListener('change', function () {
  document.getElementById('filterForm').submit();
});

