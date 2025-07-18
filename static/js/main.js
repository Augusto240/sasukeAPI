document.addEventListener('DOMContentLoaded', () => {
    const quoteText = document.getElementById('quote-text');
    const quoteContext = document.getElementById('quote-context');
    const quoteSource = document.getElementById('quote-source');
    const quoteCategory = document.getElementById('quote-category');
    const getQuoteBtn = document.getElementById('get-quote');
    const themeToggle = document.querySelector('.theme-toggle');
    const themeIcon = document.getElementById('theme-toggle-icon');
    const sharinganIcon = document.querySelector('.spin-on-click');
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    let currentCategory = 'all';
    let currentQuoteId = null;

    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.replace('light-mode', 'dark-mode');
        themeIcon.classList.replace('fa-moon', 'fa-sun');
    }

    themeToggle.addEventListener('click', () => {
        if (document.body.classList.contains('light-mode')) {
            document.body.classList.replace('light-mode', 'dark-mode');
            themeIcon.classList.replace('fa-moon', 'fa-sun');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.replace('dark-mode', 'light-mode');
            themeIcon.classList.replace('fa-sun', 'fa-moon');
            localStorage.setItem('theme', 'light');
        }
    });

    async function fetchQuote(category = 'all') {
        try {
            let url = '/sasuke/quote';
            
            if (category !== 'all') {
                const categoryResponse = await fetch(`/sasuke/quotes/category/${category}`);
                if (!categoryResponse.ok) {
                    throw new Error('Falha ao buscar citações da categoria');
                }
                
                const categoryData = await categoryResponse.json();
                if (!categoryData.quotes || categoryData.quotes.length === 0) {
                    return {
                        quote: "Não há citações nesta categoria.",
                        context: "",
                        source: "",
                        category: ""
                    };
                }
                const randomIndex = Math.floor(Math.random() * categoryData.quotes.length);
                return categoryData.quotes[randomIndex];
            } else {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error('Falha ao buscar citação');
                }
                
                return await response.json();
            }
        } catch (error) {
            console.error('Erro ao buscar citação:', error);
            return {
                quote: "Erro ao buscar citação. Por favor, tente novamente.",
                context: "",
                source: "",
                category: ""
            };
        }
    }

    async function updateQuote() {
        quoteText.style.opacity = '0.5';
        quoteContext.textContent = '';
        quoteSource.textContent = '';
        quoteCategory.textContent = '';

        sharinganIcon.classList.add('spin');

        setTimeout(async () => {
            const quoteData = await fetchQuote(currentCategory);

            setTimeout(() => {
                quoteText.textContent = quoteData.quote;
                currentQuoteId = quoteData.id;
                
                if (quoteData.context) {
                    quoteContext.textContent = `Contexto: ${quoteData.context}`;
                }
                
                if (quoteData.source) {
                    quoteSource.textContent = `Fonte: ${quoteData.source}`;
                }
                
                if (quoteData.category) {
                    quoteCategory.textContent = `Categoria: ${quoteData.category}`;
                }
                
                quoteText.style.opacity = '1';
                sharinganIcon.classList.remove('spin');
            }, 300);
        }, 700);
    }

    function setActiveCategory(category) {
        filterButtons.forEach(btn => {
            if (btn.dataset.category === category) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    getQuoteBtn.addEventListener('click', updateQuote);

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            currentCategory = btn.dataset.category;
            setActiveCategory(currentCategory);
            updateQuote();
        });
    });

    setActiveCategory('all');
    updateQuote();
});