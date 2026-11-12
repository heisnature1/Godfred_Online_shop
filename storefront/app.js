(() => {
  const products = window.PRODUCTS || [];
  const grid = document.getElementById('products');
  const search = document.getElementById('search');
  const sort = document.getElementById('sort');
  const dialog = document.getElementById('product-dialog');
  const content = document.getElementById('dialog-content');
  const money = value => `GH₵${Number(value).toFixed(2)}`;
  const currentPrice = product => product.sale_price ?? product.price;
  const slugify = text => text.toLowerCase().replace(/[^\w\s-]/g, '').trim().replace(/[\s_-]+/g, '-');
  const element = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  function image(product) {
    const img = document.createElement('img');
    img.src = product.image_url;
    img.alt = product.name;
    img.loading = 'lazy';
    img.addEventListener('error', () => { img.src = '/placeholder.svg'; }, {once: true});
    return img;
  }
  function showDetails(product) {
    content.replaceChildren();
    const detail = element('div', 'detail');
    detail.append(image(product));
    const copy = element('div', 'detail-copy');
    const title = element('h2', '', product.name);
    title.id = 'dialog-title';
    copy.append(element('p', 'eyebrow', product.category.toUpperCase()), title, element('p', 'price', money(currentPrice(product))));
    if (product.sale_price != null) {
      const oldPrice = element('del', '', money(product.price));
      copy.lastChild.append(' ', oldPrice);
    }
    copy.append(element('p', '', product.description), element('p', 'notice', 'This is a catalog preview. Ordering and checkout are not available yet.'));
    detail.append(copy);
    content.append(detail);
    if (!dialog.open) dialog.showModal();
  }
  function card(product) {
    const card = element('article', 'product');
    const picture = element('button', 'product-image');
    picture.type = 'button';
    picture.setAttribute('aria-label', `View ${product.name} details`);
    picture.addEventListener('click', () => showDetails(product));
    if (product.sale_price != null) picture.append(element('span', 'badge', 'SALE'));
    else if (product.featured) picture.append(element('span', 'badge', 'FEATURED'));
    picture.append(image(product));
    const meta = element('div', 'product-meta');
    const info = element('div');
    const name = element('button', 'product-name', product.name);
    name.type = 'button';
    name.addEventListener('click', () => showDetails(product));
    info.append(element('span', 'product-category', product.category), name);
    const prices = element('div', 'prices', money(currentPrice(product)));
    if (product.sale_price != null) prices.append(element('del', '', money(product.price)));
    meta.append(info, prices);
    const footer = element('div', 'product-footer');
    const details = element('button', '', 'View details');
    details.type = 'button';
    details.addEventListener('click', () => showDetails(product));
    footer.append(details);
    card.append(picture, meta, footer);
    return card;
  }
  function render() {
    const query = search.value.trim().toLowerCase();
    const filtered = products.filter(product => `${product.name} ${product.category} ${product.description}`.toLowerCase().includes(query));
    if (sort.value === 'low') filtered.sort((a, b) => currentPrice(a) - currentPrice(b));
    else if (sort.value === 'high') filtered.sort((a, b) => currentPrice(b) - currentPrice(a));
    else if (sort.value === 'name') filtered.sort((a, b) => a.name.localeCompare(b.name));
    else filtered.sort((a, b) => Number(b.featured) - Number(a.featured));
    grid.replaceChildren(...filtered.map(card));
    document.getElementById('count').textContent = `(${filtered.length})`;
    document.getElementById('empty').hidden = filtered.length > 0;
  }
  const params = new URLSearchParams(location.search);
  search.value = params.get('q') || '';
  if (params.get('sort') === 'price') sort.value = 'low';
  search.addEventListener('input', render);
  sort.addEventListener('change', render);
  const navSearch = document.querySelector('.nav-search');
  const navInput = document.getElementById('nav-search-input');
  navSearch.addEventListener('submit', event => {
    event.preventDefault();
    search.value = navInput.value;
    render();
    document.getElementById('shop').scrollIntoView();
  });
  document.getElementById('deals-link').addEventListener('click', () => {
    sort.value = 'low';
    render();
  });
  const menu = document.querySelector('.menu-toggle');
  const sidebar = document.getElementById('sidebar');
  function closeMenu() {
    sidebar.classList.remove('open');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', 'Open navigation');
  }
  menu.addEventListener('click', () => {
    const open = sidebar.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  sidebar.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenu();
  });
  document.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  document.getElementById('year').textContent = new Date().getFullYear();
  render();
  const parts = location.pathname.split('/').filter(Boolean);
  if (parts[0] === 'store' && parts[1] === 'products' && parts[2]) {
    const product = products.find(item => slugify(item.name) === parts[2]);
    if (product) showDetails(product);
  }
})();
