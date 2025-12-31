// State Management
let token = localStorage.getItem('access_token');

// DOM Elements
const loginCard = document.getElementById('loginCard');
const dashboard = document.getElementById('dashboard');
const userSection = document.getElementById('userSection');
const userNameDisplay = document.getElementById('userName');
const loginForm = document.getElementById('loginForm');
const postForm = document.getElementById('postForm');
const postsList = document.getElementById('postsList');

// Toast Notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastIcon = document.getElementById('toastIcon');
    const toastMessage = document.getElementById('toastMessage');

    toastMessage.innerText = message;
    toastIcon.className = type === 'success' ? 'fas fa-check-circle text-green-400' : 'fas fa-exclamation-circle text-red-400';
    
    toast.classList.remove('translate-y-20', 'opacity-0');
    setTimeout(() => {
        toast.classList.add('translate-y-20', 'opacity-0');
    }, 3000);
}

// Auth Functions
async function login(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('password', document.getElementById('password').value);

    try {
        const response = await fetch('/token', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Usuário ou senha inválidos');

        const data = await response.json();
        token = data.access_token;
        localStorage.setItem('access_token', token);
        showToast('Bem-vindo de volta!');
        checkAuth();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function logout() {
    localStorage.removeItem('access_token');
    token = null;
    checkAuth();
    showToast('Até logo!');
}

async function checkAuth() {
    if (token) {
        try {
            const response = await fetch('/me', {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const user = await response.json();
                userNameDisplay.innerText = user.username;
                loginCard.classList.add('hidden');
                dashboard.classList.remove('hidden');
                userSection.classList.remove('hidden');
                loadPosts();
            } else {
                throw new Error('Sessão expirada');
            }
        } catch (error) {
            logout();
        }
    } else {
        loginCard.classList.remove('hidden');
        dashboard.classList.add('hidden');
        userSection.classList.add('hidden');
    }
}

// CRUD Functions
async function loadPosts() {
    try {
        const response = await fetch('/posts/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const posts = await response.json();
        
        postsList.innerHTML = posts.map(post => `
            <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow group">
                <div class="flex justify-between items-start">
                    <div>
                        <h4 class="text-lg font-bold text-slate-800">${post.title}</h4>
                        <p class="text-slate-500 text-sm mt-1">
                            <i class="far fa-calendar-alt mr-1"></i> ${new Date(post.published_at).toLocaleDateString()}
                            ${post.published ? '<span class="ml-2 text-green-500 font-medium">Publicado</span>' : '<span class="ml-2 text-amber-500 font-medium">Rascunho</span>'}
                        </p>
                    </div>
                    <button onclick="deletePost(${post.id})" class="text-slate-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
                <p class="text-slate-600 mt-4 leading-relaxed">${post.content}</p>
            </div>
        `).join('') || '<p class="text-center text-slate-400 py-10">Nenhum post encontrado.</p>';
    } catch (error) {
        showToast('Erro ao carregar posts', 'error');
    }
}

async function createPost(e) {
    e.preventDefault();
    const payload = {
        title: document.getElementById('postTitle').value,
        content: document.getElementById('postContent').value,
        published: document.getElementById('postPublished').checked
    };

    try {
        const response = await fetch('/posts/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Erro ao criar post');

        showToast('Post criado com sucesso!');
        postForm.reset();
        loadPosts();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function deletePost(id) {
    if (!confirm('Tem certeza que deseja excluir este post?')) return;

    try {
        const response = await fetch(`/posts/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('Erro ao excluir post');

        showToast('Post excluído!');
        loadPosts();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// Event Listeners
loginForm.addEventListener('submit', login);
postForm.addEventListener('submit', createPost);

// Initial Check
checkAuth();
