    // Auto-redirect based on browser language (only on first visit)
    (function() {
        if (localStorage.getItem('picete_lang_choice')) return;
        
        var lang = (navigator.language || navigator.userLanguage || '').toLowerCase();
        var target = 'en';
        
        if (lang.startsWith("zh")) target = "zh";
        else if (lang.startsWith("ja")) target = "ja";
        else if (lang.startsWith("de")) target = "de";
        else if (lang.startsWith("fr")) target = "fr";
        else if (lang.startsWith("es")) target = "es";
        else if (lang.startsWith("pt")) target = "pt";
        else if (lang.startsWith("ar")) target = "ar";
        
        if (target !== 'en') {
            localStorage.setItem('picete_lang_choice', target);
            window.location.href = '/' + target + '/';
        }
    })();