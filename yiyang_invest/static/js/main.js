/**
 * 益阳高新区智慧招商平台 — 通用 JS
 */
(function () {
  'use strict';

  /* ---------- 侧栏切换（移动端） ---------- */
  window.toggleSidebar = function () {
    var sidebar = document.getElementById('sidebar');
    if (!sidebar) return;
    sidebar.classList.toggle('open');
    var overlay = document.querySelector('.sidebar-overlay');
    if (overlay) overlay.style.display = sidebar.classList.contains('open') ? 'block' : '';
    document.body.style.overflow = sidebar.classList.contains('open') ? 'hidden' : '';
  };

  /* ---------- 模态框 ---------- */
  window.showModal = function (id) {
    var modal = document.getElementById(id);
    if (modal) { modal.classList.add('show'); document.body.style.overflow = 'hidden'; }
  };
  window.hideModal = function (id) {
    var modal = document.getElementById(id);
    if (modal) { modal.classList.remove('show'); document.body.style.overflow = ''; }
  };
  // 点击背景关闭
  document.addEventListener('click', function (e) {
    if (e.target.classList.contains('modal-backdrop')) {
      var modal = e.target.closest('.modal');
      if (modal) hideModal(modal.id);
    }
  });
  // ESC 关闭
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      var modals = document.querySelectorAll('.modal.show');
      modals.forEach(function (m) { m.classList.remove('show'); });
      document.body.style.overflow = '';
    }
  });

  /* ---------- 关闭模态框按钮 ---------- */
  document.querySelectorAll('.modal-close, [data-dismiss="modal"]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var modal = btn.closest('.modal');
      if (modal) hideModal(modal.id);
    });
  });

  /* ---------- AJAX 表单提交 ---------- */
  window.submitForm = function (url, formData, callback) {
    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data.ok) { callback(null, data); }
        else { callback(data.msg || '操作失败', data); }
      })
      .catch(function (err) { callback(err.message); });
  };

  window.putJSON = function (url, data, callback) {
    fetch(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.ok) { callback(null, d); }
        else { callback(d.msg || '操作失败', d); }
      })
      .catch(function (err) { callback(err.message); });
  };

  /* ---------- 表单数据收集 ---------- */
  window.formToJSON = function (form) {
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    return data;
  };

  /* ---------- 数字格式化 ---------- */
  window.fmtAmount = function (n) {
    if (n >= 10000) return (n / 10000).toFixed(1) + ' 亿';
    if (n >= 1000) return (n / 10000).toFixed(2) + ' 万';
    return n.toFixed(0) + ' 万';
  };

  /* ---------- 日期格式化 ---------- */
  window.fmtDate = function (s) {
    if (!s) return '-';
    return s.slice(0, 10);
  };

})();
