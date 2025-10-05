document.getElementById('load').addEventListener('click', async () => {
  try {
    const res = await fetch('/api/products_get?skip=0&limit=10');
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    document.getElementById('items').innerHTML =
      data.map(x => `<tr><td>${x.id ?? ''}</td><td>${x.name ?? ''}</td></tr>`).join('');
  } catch (e) {
    console.error(e);
    alert('Error loading products');
  }
});