var RenderCategoryPage = function () {
    Category.show_category_page(window.category_data.category ? window.category_data.category : "",
                                window.category_data.topic ? window.category_data.topic : undefined);
};
