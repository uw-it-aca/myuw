import {fetchBuilder, extractData, buildWith} from './model_builder';

function compareFn(a, b) {
    const priority = ['UAA Advising', 'OMAD Advising', 'UW Honors'];
    const aPriority = (
        priority.includes(a.program) ? priority.indexOf(a.program) : priority.length);
    const bPriority = (
        priority.includes(b.program) ? priority.indexOf(b.program) : priority.length);
    return aPriority - bPriority;
};

const postProcess = (response) => {
    if (response.data && response.data.length) {
        let advisers = [];
        response.data.forEach((adv) => {
            if (adv.is_active) {
                advisers.push(adv);
            }
        });
        return advisers.sort(compareFn);
    }
    return response;
};

const customActions = {
    fetch: fetchBuilder('/api/v1/advisers/', postProcess, 'json'),
};

export default buildWith(
    {customActions},
);
