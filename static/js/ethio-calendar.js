const ethMonths = [
    "Meskerem", "Tikimt", "Hidar", "Tahsas", "Tir", "Yakatit", 
    "Maggabit", "Miyazya", "Ginbot", "Sene", "Hamle", "Nehasse", "Pagume"
];

function ecToGc(ey, em, ed) {
    let days = 0;
    if (ey >= 2016) {
        for(let y = 2016; y < ey; y++) {
            days += (y % 4 === 3) ? 366 : 365;
        }
    } else {
        for(let y = 2015; y >= ey; y--) {
            days -= (y % 4 === 3) ? 366 : 365;
        }
    }
    days += (em - 1) * 30;
    days += (ed - 1);
    let anchor = new Date(Date.UTC(2023, 8, 12)); // Sep 12, 2023 is EC 2016-01-01
    anchor.setUTCDate(anchor.getUTCDate() + days);
    return anchor.toISOString().split('T')[0];
}

function gcToEc(gcDate) {
    let anchor = new Date(Date.UTC(2023, 8, 12));
    let diffTime = gcDate.getTime() - anchor.getTime();
    let days = Math.floor(diffTime / 86400000);
    
    let ey = 2016;
    if (days >= 0) {
        while (true) {
            let yearDays = (ey % 4 === 3) ? 366 : 365;
            if (days >= yearDays) {
                days -= yearDays;
                ey++;
            } else {
                break;
            }
        }
    } else {
        while (days < 0) {
            ey--;
            let yearDays = (ey % 4 === 3) ? 366 : 365;
            days += yearDays;
        }
    }
    
    let em = Math.floor(days / 30) + 1;
    let ed = (days % 30) + 1;
    if (em > 13) {
        ed += (em - 13) * 30;
        em = 13;
    }
    return {ey, em, ed};
}

// Initialize on all inputs with class 'ethiopian-date'
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.ethiopian-date').forEach(input => {
        // Hide the original input
        input.style.display = 'none';
        
        const wrapper = document.createElement('div');
        wrapper.className = 'ethio-date-wrapper';
        wrapper.style.display = 'flex';
        wrapper.style.gap = '0.5rem';
        
        const todayGC = new Date();
        const todayEC = gcToEc(todayGC);
        
        // Initialize state
        let currentEC = { ...todayEC };
        if (input.value) {
            let [y, m, d] = input.value.split('-');
            if (y && m && d) {
                currentEC = gcToEc(new Date(Date.UTC(parseInt(y), parseInt(m)-1, parseInt(d))));
            }
        } else {
            input.value = ecToGc(todayEC.ey, todayEC.em, todayEC.ed);
        }

        const selMonth = document.createElement('select');
        selMonth.className = 'ethio-month';
        ethMonths.forEach((mName, i) => {
            const opt = document.createElement('option');
            opt.value = i + 1;
            opt.textContent = mName;
            selMonth.appendChild(opt);
        });
        selMonth.value = currentEC.em;

        const selDay = document.createElement('select');
        selDay.className = 'ethio-day';
        const updateDays = () => {
            let maxDays = 30;
            if (parseInt(selMonth.value) === 13) {
                maxDays = (parseInt(selYear.value) % 4 === 3) ? 6 : 5;
            }
            let oldDay = parseInt(selDay.value) || currentEC.ed;
            selDay.innerHTML = '';
            for(let i=1; i<=maxDays; i++) {
                const opt = document.createElement('option');
                opt.value = i;
                opt.textContent = i;
                selDay.appendChild(opt);
            }
            if (oldDay > maxDays) oldDay = maxDays;
            selDay.value = oldDay;
        };

        const selYear = document.createElement('select');
        selYear.className = 'ethio-year';
        for(let i = todayEC.ey - 2; i <= todayEC.ey + 5; i++) {
            const opt = document.createElement('option');
            opt.value = i;
            opt.textContent = i;
            selYear.appendChild(opt);
        }
        selYear.value = currentEC.ey;

        updateDays();
        
        // Style them
        [selMonth, selDay, selYear].forEach(sel => {
            sel.style.flex = '1';
            sel.style.background = 'var(--dark-3)';
            sel.style.border = '1px solid var(--border)';
            sel.style.color = 'var(--text)';
            sel.style.padding = '0.7rem';
            sel.style.borderRadius = 'var(--radius-sm)';
            sel.style.outline = 'none';
        });

        // Event listener
        const updateVal = () => {
            updateDays();
            const gcDateStr = ecToGc(parseInt(selYear.value), parseInt(selMonth.value), parseInt(selDay.value));
            input.value = gcDateStr;
            // Dispatch change event on original input
            input.dispatchEvent(new Event('change'));
        };

        selMonth.addEventListener('change', updateVal);
        selYear.addEventListener('change', updateVal);
        selDay.addEventListener('change', () => {
            const gcDateStr = ecToGc(parseInt(selYear.value), parseInt(selMonth.value), parseInt(selDay.value));
            input.value = gcDateStr;
            input.dispatchEvent(new Event('change'));
        });

        wrapper.appendChild(selMonth);
        wrapper.appendChild(selDay);
        wrapper.appendChild(selYear);
        
        input.parentNode.insertBefore(wrapper, input.nextSibling);
    });
});
