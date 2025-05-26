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

  // 👥 Toggle follower/seguiti (Profile)
  const opt1 = document.getElementById('opt1');
  const opt2 = document.getElementById('opt2');
  const followerList = document.getElementById('follower-list');
  const seguitiList = document.getElementById('seguiti-list');
  if (opt1 && opt2 && followerList && seguitiList) {
    opt1.addEventListener('change', function () {
      if (opt1.checked) {
        followerList.style.display = 'block';
        seguitiList.style.display = 'none';
      }
    });
    opt2.addEventListener('change', function () {
      if (opt2.checked) {
        followerList.style.display = 'none';
        seguitiList.style.display = 'block';
      }
    });
  }

  const inputRicerca = document.querySelector('.barra-ricerca input[type="text"]');
  if (inputRicerca) {
    inputRicerca.focus();
  }
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

