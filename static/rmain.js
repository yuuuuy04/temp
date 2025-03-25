const myHeaders = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "128",
    "Content-Type": "application/json",
    "Host": "localhost:5000",
    "Origin": "http://127.0.0.1:5500",
    "Referer": "http://127.0.0.1:5500/",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}
document.addEventListener('DOMContentLoaded',async function() {
    let loadSrcResponse=await fetch("http://localhost:5000/loadSrc",{
        method: "GET",
        // headers: myHeaders,
        // body: JSON.stringify({'region':region,'update':selectedUpdateTime })
    });
    if (loadSrcResponse.ok){
        let imgData = await loadSrcResponse.json();
        console.log(imgData['data']['src'])
        console.log(imgData)
        document.getElementById('user-logo').src = imgData['data']['src'];
       
    }
    // const signal = 'need_img_src';checkCoolaborated
    // fetch('http://localhost:5000/checkCoolaborated', {
    //     method: 'GET',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     // body: JSON.stringify({single: signal})
    // })
    // .then(response => response.json())
    // .then(data => {
    //     // 在这里处理返回的数据，比如更新img标签的src属性
    //     document.getElementById('user-logo').src = data.src;
    // })
    // .catch(error => console.error('Error:', error));
    // fetch('http://localhost:5000/checkCoolaborated', {
    //     method: 'GET'
    // })
    // .then(response => {
    //     if (!response.ok) {
    //         throw new Error('Network response was not ok ' + response.statusText);
    //     }
    //     return response.json();
    // })
    // .then(data => {
    //     console.log(data.src); // 假设返回的数据对象中包含src属性
    //     document.getElementById('user-logo').src = data.src; // 使用返回的数据更新页面上的元素
    // })
    // .catch(error => console.error('There was a problem with the fetch operation:', error));
});
// 顶部地区选择
let region='MY'
const regionSelectMenu=document.querySelector('.top-right-slider')
const regionSelectRadio=document.querySelector('.top-right-slider .region-select-radio')
const regionSelectBar=document.querySelector('.top-right-slider-region')
const shopName=document.querySelector('.top-slider .top-right-slider .shop-name')
regionSelectMenu.addEventListener('click',function(){
    if(regionSelectBar.classList.contains('region-hidden')){
        regionSelectBar.classList.remove('region-hidden')
    }else{
        regionSelectBar.classList.add('region-hidden') 
        
    }
})
document.querySelectorAll('.top-right-slider-region .region-select-radio').forEach(function(radio) {
    radio.addEventListener('change', function() {
        if (this.checked) {
            console.log(this.value) // 当前选中的单选按钮的值
            shopName.innerHTML=this.value
            region=this.value
            regionSelectBar.classList.add('region-hidden') 
        }
    });
});
// 左侧菜单导航栏
const navSliderBar=document.querySelector('.left-slider .menu')
navSliderBar.addEventListener('click',function(e){
    if (e.target.tagName==='LI'){
        let element_active_li = document.querySelector('.left-slider .menu li.menu-active')
        if (element_active_li) {
            element_active_li.classList.remove('menu-active')
        }
        e.target.classList.add('menu-active')
        let index = e.target.dataset.id
        let boxContianerActive=document.querySelector('.main-content-box >.unhidden')
        if (boxContianerActive){
            boxContianerActive.classList.remove('unhidden')
        }
        let boxContianer=document.querySelector(`.main-content-box .box${index}`)
        boxContianer.classList.add('unhidden')
    }
})

// load-data
const loadData=document.querySelector('.load-data .load-condition .submit-button')
const loadOverlay=document.querySelector('.load-overlay')
const loadGif=document.querySelector('.load-gif')
const resultShowLoadData=document.querySelector('.main-content-box .load-data .finish')
function getSelectedRadioValue(name) {
    // 获取所有与'name'参数相匹配的单选按钮
    const radios = document.getElementsByName(name);
    let selectedValue;

    // 遍历每个单选按钮，查找是否有被选中的
    for (let i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            // 如果单选按钮被选中，则将其值赋给selectedValue并跳出循环
            selectedValue = radios[i].value;
            break;
        }
    }
    if (selectedValue === undefined) {
        selectedValue = 'isNoSelect'
    }
    return selectedValue; // 返回选中的单选按钮的值或undefined
}
loadData.addEventListener('click',async function(){
    const selectedUpdateTime = getSelectedRadioValue('update-time')
    console.log('用户选择的更新时间为:', selectedUpdateTime)
    console.log('用户选择的店铺地区是:',region)
    if(selectedUpdateTime==='isNoSelect'){
        alert('未选择更新时间')
    }else{
        loadOverlay.classList.remove('hidden')
        loadGif.classList.remove('hidden')
        let loadDataResponse=await fetch("http://localhost:5000/loadData",{
            method: "POST",
            headers: myHeaders,
            body: JSON.stringify({'region':region,'update':selectedUpdateTime })
        });
        if (loadDataResponse.ok){
            loadOverlay.classList.add('hidden')
            loadGif.classList.add('hidden')
            resultShowLoadData.classList.remove('hidden')
        }
    }
})

// 隐藏details
document.addEventListener('click', function (e) {
    // 获取所有的details元素
    let allDetails = document.querySelectorAll('.main-content-box .box2 .select-box .select-option ul li .details.unhidden');
    
    // 尝试获取被点击的li元素
    const clickedLi = e.target.closest('li'); // 注意这里的'LI'应为小写的'li'
    
    if (clickedLi) { // 如果点击的是li标签或其子元素
        // 获取当前li下的details元素
        let boxSelectContainer = document.querySelector(`.main-content-box .box2 .select-box .select-option ul li[data-id="${clickedLi.dataset.id}"] .details`);
        
        // 检查是否点击在已经展开的details内部
        let isClickInDetails = e.target.closest('.details.unhidden');

        if (!isClickInDetails) {
            // 隐藏所有展开的details（除了当前正在操作的）
            allDetails.forEach(detail => {
                if (detail !== boxSelectContainer) {
                    detail.classList.remove('unhidden');
                }
            });

            if (boxSelectContainer) { // 确保找到对应的details
                // 切换对应的details显示状态
                boxSelectContainer.classList.toggle('unhidden');
            }
        } else {
            // 如果点击发生在已展开的details内部，则不做处理，保持展开状态
        }
    } else {
        // 如果点击的不是li元素，则隐藏所有展开的details
        allDetails.forEach(detail => {
            detail.classList.remove('unhidden');
        });
    }
});

// 在rmain.js中添加以下代码
const minInputFans=document.querySelector('.main-content-box .send-data .select-box .select-option ul .details .min-input.fans')
const maxInputFans=document.querySelector('.main-content-box .send-data .select-box .select-option ul .details .max-input.fans')
console.log(minInputFans.value,maxInputFans.value)


function setupRangeInputs(selector) {
    document.querySelectorAll(selector).forEach(input => {
        input.addEventListener('blur', function() { // 使用'blur'代替'input'
            const container = input.closest('.range-inputs');
            const minInput = container.querySelector('.min-input');
            const maxInput = container.querySelector('.max-input');

            let minValue = parseFloat(minInput.value);
            let maxValue = parseFloat(maxInput.value);

            // 获取默认的min和max属性值
            const defaultMin = parseFloat(minInput.min);
            const defaultMax = parseFloat(maxInput.max);

            // 如果输入无效，则取默认min/max值
            if (isNaN(minValue) || minValue < defaultMin || minValue > defaultMax) {
                minValue = defaultMin;
                minInput.value = minValue;
            }
            if (isNaN(maxValue) || maxValue < defaultMin || maxValue > defaultMax) {
                maxValue = defaultMax;
                maxInput.value = maxValue;
            }

            // 当max值小于min值时，交换它们
            if (maxValue < minValue) {
                [minInput.value, maxInput.value] = [maxValue, minValue];
            }
        });
    });
}

// 调用函数，传入需要处理的选择器
setupRangeInputs('.commission-rate, .fans, .GMV, .video-play-num, .promote-product-num, .video-publish-num');


// 重置条件
document.querySelector('.main-content-box .send-data .reset-condition-button').addEventListener('click', function() {
    // 重置商品类目复选框
    document.querySelectorAll('.select-box-201 input[type="checkbox"]').forEach(function(checkbox) {
        checkbox.checked = false;
    });
    // 通用函数来重置范围输入框
    function resetRangeInputs(minInputSelector, maxInputSelector) {
        let minInput = document.querySelector(minInputSelector);
        let maxInput = document.querySelector(maxInputSelector);
        minInput.value = minInput.min;
        maxInput.value = maxInput.max;
    }
    // 重置粉丝数范围输入框
    resetRangeInputs('.main-content-box .send-data .select-box-202 .min-input.fans', '.select-box-202 .max-input.fans');
    // 重置中位佣金率范围输入框
    resetRangeInputs('.main-content-box .send-data .select-box-203 .min-input.commission-rate', '.select-box-203 .max-input.commission-rate');
    // 重置视频GMV范围输入框
    resetRangeInputs('.main-content-box .send-data .select-box-204 .min-input.GMV', '.select-box-204 .max-input.GMV');
    // 重置视频播放量范围输入框
    resetRangeInputs('.main-content-box .send-data .select-box-205 .min-input.video-play-num', '.select-box-205 .max-input.video-play-num');
    // 重置推广产品数量范围输入框
    resetRangeInputs('.main-content-box .send-data .select-box-206 .min-input.promote-product-num', '.select-box-206 .max-input.promote-product-num');
    // 重置视频发布次数范围输入框
    resetRangeInputs('.main-content-box .send-data .select-box-207 .min-input.video-publish-num', '.select-box-207 .max-input.video-publish-num');
    // 重置是否邀请过复选框
    document.getElementById('is-invite').checked = false;
});

const sortBox = document.querySelector('.main-content-box .send-data .sort-reason .sort-box');
const sortReasonBox = document.querySelector('.main-content-box .send-data .sort-reason .sort-box .sort-reason-box');
const sortReasonResult = document.querySelector('.main-content-box .send-data .sort-reason .sort-box .sort-reason-result'); 
// 排序依据3个功能
// 切换 'unhidden' 类
sortBox.addEventListener('click', function () {
    if (sortReasonBox.classList.contains('unhidden')) {
        sortReasonBox.classList.remove('unhidden');
    } else {
        sortReasonBox.classList.add('unhidden');
    }
});

// 功能2: 监听对 li 的点击事件
sortReasonBox.addEventListener('click', function (event) {
    if (event.target.tagName === 'LI') {
        // 移除所有 li 中的 'mark' 类
        Array.from(sortReasonBox.querySelectorAll('li')).forEach(function (li) {
            li.classList.remove('mark');
        });
        // 给被点击的 li 添加 'mark' 类
        event.target.classList.add('mark');
        // 更新 sort-reason-result 的文本内容
        sortReasonResult.textContent = event.target.textContent;
        let sortByField = mapSortReasonToField(sortReasonResult.textContent)
        let sortedData = sortDataList(parsedData, sortByField);
        renderSortTable(sortedData)
        console.log(`Sorted by ${sortByField}:`, sortedData)
    }
});

// 功能3: 点击任意位置移除 'unhidden'
document.addEventListener('click', function (event) {
    if (!event.target.closest('.main-content-box .send-data .sort-reason .sort-box .sort-reason-box') && 
    !event.target.closest('.main-content-box .send-data .sort-reason .sort-box')) {
        if (sortReasonBox.classList.contains('unhidden')) {
            sortReasonBox.classList.remove('unhidden');
        }
    }
});

function sortDataList(dataList, sortByField) {
    // 检查输入的有效性
    if (!dataList || dataList.length <= 1) return dataList;
    if (sortByField === '综合得分') {
        // 智能排序已由后端完成，直接使用原始顺序
        return dataList;
    }
    // 创建一个新的数组以避免修改原始数据
    let sortedList = [...dataList];

    // 对数组进行排序，数值高者在前
    sortedList.sort((a, b) => {
        if (a[sortByField] === undefined || b[sortByField] === undefined) {
            console.warn(`Warning: One of the items does not contain the field ${sortByField}`);
            return 0;
        }
        // 转换为数字进行比较，确保正确处理字符串数字
        return parseFloat(b[sortByField]) - parseFloat(a[sortByField]);
    });
    return sortedList;
}

/**
 * 根据前端显示的文字描述映射到后端数据字段名称
 * @param {String} sortReason - 前端显示的文字描述，如 '商品交易总额', '粉丝数'
 * @returns {String|undefined} 对应的数据字段名称或undefined
 */

function mapSortReasonToField(sortReason) {
    const reasonToFieldMap = {
        "商品交易总额": "视频GMV（商品交易总额）",
        "粉丝数": "粉丝数",
        "成交件数": "成交件数" ,
        "智能推荐":"综合得分"
    };

    return reasonToFieldMap[sortReason] || undefined;
}


var parsedData=[]

function renderSortTable(parsedData) {
    const tbody = document.querySelector('#sort-table tbody'); // 获取表格的tbody元素
    
    if (!tbody) {
        console.error('Tbody element not found');
        return;
    }

    // 清空现有的tbody内容
    tbody.innerHTML = '';
    let rank = 1; // 定义一个排名变量
    parsedData.forEach(item => {
        const row = document.createElement('tr');
        row.id = `${item['达人ID']}`; // 设置 tr 的 id 属性为达人ID
        let rankCell = document.createElement('td');
        rankCell.innerHTML = `<input type="checkbox"><span class="rank">${rank}</span>`;
        row.appendChild(rankCell);
        rank++; // 每处理一行，排名递增
        // 创建复选框单元格
        // let checkboxCell = document.createElement('td');
        // let checkbox = document.createElement('input');
        // checkbox.type = "checkbox";
        // checkboxCell.appendChild(checkbox);
        // row.appendChild(checkboxCell);

        // 添加达人ID
        // row.insertAdjacentHTML('beforeend', `<td>${item['达人ID']}</td>`);

        // 添加达人用户名
        row.insertAdjacentHTML('beforeend', `<td>${item['达人用户名']}</td>`);
        // 添加视频GMV（商品交易总额）
        row.insertAdjacentHTML('beforeend', `<td>${item['视频GMV（商品交易总额）']}</td>`);
        // 添加粉丝数
        // row.insertAdjacentHTML('beforeend', `<td>${item['粉丝数']}</td>`);
        // 添加推广的产品数量
        row.insertAdjacentHTML('beforeend', `<td>${item['推广的产品数量']}</td>`);
        row.insertAdjacentHTML('beforeend', `<td>${item['视频平均播放次数']}</td>`);
        row.insertAdjacentHTML('beforeend', `<td>${item['中位佣金率']}</td>`);

        // 添加操作列，包含SVG图标
        row.insertAdjacentHTML('beforeend', `
            <td>
                <svg class="icon" style="width: 1em;height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2552">
                    <path d="M510.5278 131.208c181.168 0 346.344 110.536 495.52 331.632a87.872 87.872 0 0 1 3.296 93.032l-3.296 5.272-8.36 12.192c-146.976 213.024-309.36 319.504-487.168 319.44-181.248 0-346.424-110.544-495.52-331.632a87.888 87.888 0 0 1-3.296-92.928l3.296-5.376 8.352-12.088c146.912-213.032 309.304-319.544 487.176-319.544z m0 87.888c-145.216 0-282.968 90.28-414.672 281.096l-8.016 11.864 8.128 11.752c131.816 190.912 269.456 281.096 414.56 281.096 145.104 0 282.848-90.296 414.568-281.096l8.568-11.752-8.024-11.864c-132.368-190.92-270-281.096-415.112-281.096z m0 106.432c107.256-1.304 195.272 84.576 196.568 191.84 1.312 107.272-84.584 195.28-191.848 196.576a30.984 30.984 0 0 1-4.72 0c-107.264 0-194.216-86.952-194.216-194.2 0.008-107.256 86.96-194.216 194.216-194.216z m0 87.88c-58.728-0.968-107.12 45.848-108.096 104.576-0.968 58.72 45.848 107.12 104.576 108.088 1.168 0.104 2.344 0.104 3.512 0 58.72-0.016 106.312-47.64 106.296-106.368-0.008-58.704-47.592-106.28-106.288-106.296z" fill="#17A29E" p-id="2553"></path>
                </svg>
            </td>
        `);

        // 将生成的行添加到tbody中
        tbody.appendChild(row);
    });
    updateCheckedCount();
    // 获取所有的svg元素作为触发器
    const svgTriggers = document.querySelectorAll('#sort-table tbody svg');
    svgTriggers.forEach(svg => {
        svg.addEventListener('click', function(event) {
            console.log("眼")
            event.stopPropagation(); // 防止事件冒泡到文档
            const trElement = this.closest('tr'); // 找到最近的祖先tr元素
            if (trElement) {
                showCreatorDetails(trElement.id);
            }
        });
});
}
document.querySelector('.main-content-box .send-data .start-filter-button').addEventListener('click', async function() {
    // 创建一个对象来存储所有的筛选条件
    const filterConditions = {
        // 原有筛选条件...
        need_smart_rank: true,  // 新增参数
        model_type: 'AHP'       // 指定排序模型
    };
    
    // 收集商品类目筛选条件
    filterConditions.selectedCategories = [];
    document.querySelectorAll('.main-content-box .send-data .select-box-201 input[type="checkbox"]').forEach(function(checkbox) {
        if (checkbox.checked) {
            filterConditions.selectedCategories.push(checkbox.value);
        }
    });

    // 粉丝数范围
    const maxFansInput = document.querySelector('.main-content-box .send-data .select-box-202 .max-input.fans');
    filterConditions.minFans = parseFloat(document.querySelector('.main-content-box .send-data .select-box-202 .min-input.fans').value);
    filterConditions.maxFans = maxFansInput.value === maxFansInput.max ? "ismax" : parseFloat(maxFansInput.value);

    // 中位佣金率范围
    const maxCommissionRateInput = document.querySelector('.main-content-box .send-data .select-box-203 .max-input.commission-rate');
    filterConditions.minCommissionRate = parseFloat(document.querySelector('.main-content-box .send-data .select-box-203 .min-input.commission-rate').value);
    filterConditions.maxCommissionRate = maxCommissionRateInput.value === maxCommissionRateInput.max ? "ismax" : parseFloat(maxCommissionRateInput.value);

    // 视频GMV范围
    const maxGMVInput = document.querySelector('.main-content-box .send-data .select-box-204 .max-input.GMV');
    filterConditions.minGMV = parseFloat(document.querySelector('.main-content-box .send-data .select-box-204 .min-input.GMV').value);
    filterConditions.maxGMV = maxGMVInput.value === maxGMVInput.max ? "ismax" : parseFloat(maxGMVInput.value);

    // 平均视频播放量范围
    const maxVideoPlayNumInput = document.querySelector('.main-content-box .send-data .select-box-205 .max-input.video-play-num');
    filterConditions.minVideoPlayNum = parseFloat(document.querySelector('.main-content-box .send-data .select-box-205 .min-input.video-play-num').value);
    filterConditions.maxVideoPlayNum = maxVideoPlayNumInput.value === maxVideoPlayNumInput.max ? "ismax" : parseFloat(maxVideoPlayNumInput.value);

    // 推广产品数量范围
    const maxPromoteProductNumInput = document.querySelector('.main-content-box .send-data .select-box-206 .max-input.promote-product-num');
    filterConditions.minPromoteProductNum = parseInt(document.querySelector('.main-content-box .send-data .select-box-206 .min-input.promote-product-num').value, 10);
    filterConditions.maxPromoteProductNum = maxPromoteProductNumInput.value === maxPromoteProductNumInput.max ? "ismax" : parseInt(maxPromoteProductNumInput.value, 10);

    // 视频发布次数范围
    const maxVideoPublishNumInput = document.querySelector('.main-content-box .send-data .select-box-207 .max-input.video-publish-num');
    filterConditions.minVideoPublishNum = parseInt(document.querySelector('.main-content-box .send-data .select-box-207 .min-input.video-publish-num').value, 10);
    filterConditions.maxVideoPublishNum = maxVideoPublishNumInput.value === maxVideoPublishNumInput.max ? "ismax" : parseInt(maxVideoPublishNumInput.value, 10);

    // 是否邀请过
    filterConditions.isInvite = document.getElementById('is-invite').checked;

    console.log("筛选条件:", filterConditions);
    let filterDataResponse = await fetch("http://localhost:5000/filterData",{
        method: "POST",
        headers: myHeaders,
        body: JSON.stringify({
            'filterCondition': filterConditions,
            'sortBy': 'smart'  // 新增排序标识
        })
    });
    if (filterDataResponse.ok) {
        // 解析返回的JSON数据
        let filterData = await filterDataResponse.json();
        const sortReason=document.querySelector('.main-content-box .send-data .sort-reason')
        const displayCraetorBox=document.querySelector('.main-content-box .send-data .display-creator-box')
        const sendInfoBox=document.querySelector('.main-content-box .send-data .send-info-box')
        sortReason.classList.add('unhidden')
        displayCraetorBox.classList.add('unhidden')
        sendInfoBox.classList.add('unhidden')
        // 假设后端返回的数据结构为{'data': "[{...},{...}]"}，需要将字符串转换回数组
        parsedData = JSON.parse(filterData.filter_data);
    
        console.log('filter ok');
        console.log('Filtered Data:', parsedData); // 打印筛选后的数据
        // 根据商品交易总额排序
        let sortByField = mapSortReasonToField(sortReasonResult.textContent)
        let sortedData = sortDataList(parsedData, sortByField);
        renderSortTable(sortedData);
        console.log(`Sorted by ${sortByField}:`, sortedData)
    } else {
        console.error('Failed to fetch filtered data:', filterDataResponse.statusText);
    }
});


// 定义一个函数用于更新选中的复选框数量
function updateCheckedCount() {
    let checkedCount = document.querySelectorAll('#sort-table tbody input[type="checkbox"]:checked').length;
    document.querySelector('.check-num').textContent = checkedCount;
}

// 监听复选框的变化，并实时更新选中的复选框数量
document.querySelector('#sort-table tbody').addEventListener('change', (event) => {
    if(event.target.type === 'checkbox') {
        updateCheckedCount(); // 更新计数
    }
});
// 点击表头复选框全选或取消全选
document.querySelector('#sort-table thead input[type="checkbox"]').addEventListener('change', function() {
    const isChecked = this.checked;
    document.querySelectorAll('#sort-table tbody input[type="checkbox"]').forEach(cb => cb.checked = isChecked);
    
    // 同时更新计数器
    document.querySelector('.check-num').textContent = isChecked ? document.querySelectorAll('#sort-table tbody input[type="checkbox"]').length : 0;
});


// 达人详细信息展示

// 获取所有的svg元素作为触发器
const svgTriggers = document.querySelectorAll('#sort-table tbody svg');
svgTriggers.forEach(svg => {
    svg.addEventListener('click', function(event) {
        console.log("眼")
        event.stopPropagation(); // 防止事件冒泡到文档
        const trElement = this.closest('tr'); // 找到最近的祖先tr元素
        if (trElement) {
            showCreatorDetails(trElement.id);
        }
    });
});

// 点击遮罩或除详情框外的任何地方时关闭详情
const displayBox = document.querySelector('.display-creator-details-box');
const maskBox = document.querySelector('.display-creator-details-mask-box');
const creatorDetailsClose=document.querySelector('.main-content-box .send-data .display-creator-details-mask-box .display-creator-details-box .fork')
document.addEventListener('click', function(event) {
    // const displayBox = document.querySelector('.display-creator-details-box');
    // const maskBox = document.querySelector('.display-creator-details-mask-box');
    if (!displayBox.contains(event.target)) {
    // if (!displayBox.contains(event.target) && !event.target.classList.contains('icon')) {
        hideCreatorDetails();
    }
});
creatorDetailsClose.addEventListener('click',function(){
    hideCreatorDetails();
})

// 显示创作者详情的函数
function showCreatorDetails(id) {
    const creatorDetails = parsedData.find(item => item['达人ID'] == id);
    if (creatorDetails) {
        const creatorDetailsContainer = document.querySelector('.display-creator-details-box');
        creatorDetailsContainer.querySelector('.craetor-name').textContent = creatorDetails['达人用户名'];
        
        // 清空之前的列表项
        const ulElement = creatorDetailsContainer.querySelector('ul');
        ulElement.innerHTML = '';

        for (const [key, value] of Object.entries(creatorDetails)) {
            if (key !== '达人ID') { // 过滤掉达人ID
                const liElement = document.createElement('li');
                liElement.innerHTML = `<span class="key">${key}</span><span class="value">${value}</span>`;
                ulElement.appendChild(liElement);
            }
        }

        // 显示遮罩层和详情框
        maskBox.classList.add('unhidden');
    }
}

// 隐藏创作者详情的函数
function hideCreatorDetails() {
    const maskBox = document.querySelector('.display-creator-details-mask-box');
    maskBox.classList.remove('unhidden');
}

// 发送框实现逻辑
const textarea = document.querySelector('textarea[data-e2e="798845f5-2eb9-0980"]');
const charCountDisplay = document.querySelector('span[data-e2e="76868bb0-0a54-15ad"]');
const sendButton = document.querySelector('button[data-tid="m4b_button"]');
const tbody = document.querySelector('#sort-table tbody');

// 实时更新字符计数
textarea.addEventListener('input', function() {
    let currentLength = textarea.value.length;
    charCountDisplay.textContent = currentLength;

    // 控制发送按钮状态
    if (charCountDisplay.textContent > 2000 || charCountDisplay.textContent == 0) {
        sendButton.disabled = true;
    } else {
        sendButton.disabled = false;
    }
});

// 发送按钮点击事件
sendButton.addEventListener('click',async function() {
    if (charCountDisplay.textContent > 2000 || charCountDisplay.textContent == 0) {
        alert('请在1~2000字内')
    } else {
        let checkedRowsIds = [];
        if (tbody) {
            tbody.querySelectorAll('input[type="checkbox"]:checked').forEach(function(checkbox) {
                checkedRowsIds.push(checkbox.closest('tr').id);
            });
        }
        if(checkedRowsIds.length===0){
            alert('请选择至少一位达人')
        } else {
            console.log("已选中的达人ID:", checkedRowsIds);
            console.log("Textarea的内容:", textarea.value);
            let sendDataResponse = await fetch("http://localhost:5000/sendData",{
                method: "POST",
                headers: myHeaders,
                body: JSON.stringify({'creator_list': checkedRowsIds,"info":textarea.value,"region":region})
            });
            if (sendDataResponse.ok) {
                let sendData = await sendDataResponse.json();
                alert(`成功发送：${textarea.value}`);
                console.log(sendData)
            }
        }
    }
});
var checkCollaboratedData
const checkCollaboratedBox = document.querySelector('body > div.left-slider > ul > li:nth-child(3)')
let checkJson=true
checkCollaboratedBox.addEventListener('click',async function () {
    if(checkJson){
        // loadOverlay.classList.remove('hidden')
        // loadGif.classList.remove('hidden')
        console.log('第三板块')
        checkJson=false
        let checkCollaboratedResponse = await fetch("http://localhost:5000/checkCoolaborated",{
            method: "POST",
            headers: myHeaders,
            body: JSON.stringify({'single': "check_json",'region':region})
        });
        if (checkCollaboratedResponse.ok) {
            checkCollaboratedData = await checkCollaboratedResponse.json();
            if(!checkCollaboratedData['single']){
                alert("请你先完成前面两模块的运行")
                checkJson=true
            }
            loadOverlay.classList.add('hidden')
            loadGif.classList.add('hidden')
        }
    }else {
        console.log("已加载过数据")
    }
})

// 获取所有的li元素
const hasCollaboratedLiElements = document.querySelectorAll('.has-collaborated-select-box ul li');
    
// 对每个li元素添加点击监听器
hasCollaboratedLiElements.forEach(li => {
    li.addEventListener('click',async function() {
        // 移除所有li的'click'类，并给当前点击的li添加'click'类
        hasCollaboratedLiElements.forEach(el => el.classList.remove('click'));
        this.classList.add('click');

        // 根据点击的li内容选择渲染规则
        let filteredCollaboratedData;
        if (this.textContent.includes('联系过的达人')) {
            filteredCollaboratedData = checkCollaboratedData['data'];
            renderCollaboratedTable(filteredCollaboratedData);
        } else if (this.textContent.includes('等待合作')) {
            filteredCollaboratedData = checkCollaboratedData['data'].filter(item => item.check[item.check.length - 1].has_collaborated === "False");
            renderCollaboratedTable(filteredCollaboratedData);
        } else if (this.textContent.includes('已合作')) {
            filteredCollaboratedData = checkCollaboratedData['data'].filter(item => item.check[item.check.length - 1].has_collaborated === "True");
            renderCollaboratedTable(filteredCollaboratedData);
        } else if (this.textContent.includes('重新获取合作信息')) {
            loadOverlay.classList.remove('hidden')
            loadGif.classList.remove('hidden')
            let checkCollaboratedResponse = await fetch("http://localhost:5000/checkCoolaborated",{
                method: "POST",
                headers: myHeaders,
                body: JSON.stringify({'single': "check_json"})
            });
            if (checkCollaboratedResponse.ok) {
                checkCollaboratedData = await checkCollaboratedResponse.json();
                console.log(checkCollaboratedData)
                if(!checkCollaboratedData['single']){
                    alert("请先执行完前2模块")
                }
                loadOverlay.classList.add('hidden')
                loadGif.classList.add('hidden')
            }
        }

        // renderCollaboratedTable(filteredCollaboratedData);
    });
});

function renderCollaboratedTable(data) {
    const tbody = document.querySelector('.main-content-box .collaborated-data .show-container table tbody');
    tbody.innerHTML = ''; // 清空现有tbody内容
    data.forEach(item => {
        const lastDetail = item.details[item.details.length - 1];
        const lastCheck = item.check[item.check.length - 1];
        const row = document.createElement('tr');
        row.id = item.id
        row.innerHTML = `
            <td>${item.nickname}</td>
            <td>${lastDetail.update}</td>
            <td><div class="scrollable-content">${lastDetail.text}</div></td>
            <td>${lastCheck.has_collaborated === "True" ? '已合作' : '未合作'}</td>
            <td>
                <svg class="icon" style="width: 1em;height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2552"><path d="M510.5278 131.208c181.168 0 346.344 110.536 495.52 331.632a87.872 87.872 0 0 1 3.296 93.032l-3.296 5.272-8.36 12.192c-146.976 213.024-309.36 319.504-487.168 319.44-181.248 0-346.424-110.544-495.52-331.632a87.888 87.888 0 0 1-3.296-92.928l3.296-5.376 8.352-12.088c146.912-213.032 309.304-319.544 487.176-319.544z m0 87.888c-145.216 0-282.968 90.28-414.672 281.096l-8.016 11.864 8.128 11.752c131.816 190.912 269.456 281.096 414.56 281.096 145.104 0 282.848-90.296 414.568-281.096l8.568-11.752-8.024-11.864c-132.368-190.92-270-281.096-415.112-281.096z m0 106.432c107.256-1.304 195.272 84.576 196.568 191.84 1.312 107.272-84.584 195.28-191.848 196.576a30.984 30.984 0 0 1-4.72 0c-107.264 0-194.216-86.952-194.216-194.2 0.008-107.256 86.96-194.216 194.216-194.216z m0 87.88c-58.728-0.968-107.12 45.848-108.096 104.576-0.968 58.72 45.848 107.12 104.576 108.088 1.168 0.104 2.344 0.104 3.512 0 58.72-0.016 106.312-47.64 106.296-106.368-0.008-58.704-47.592-106.28-106.288-106.296z" fill="#17A29E" p-id="2553"></path></svg>
            </td>
        `;
        tbody.appendChild(row);
    });

    // 功能2：为每个svg添加点击事件
    const collaboratedSvgs = document.querySelectorAll('.collaborated-data table svg');
    collaboratedSvgs.forEach(svg => {
        svg.addEventListener('click', function(event) {
            event.stopPropagation();
            const creatorId = this.closest('tr').id;
            const maskBox = document.querySelector('.display-collaborated-details-mask-box');
            maskBox.classList.add('unhidden');
            renderCollaboratedDetails(creatorId); // 调用渲染函数
        });
    });
}

// 功能3：详情弹窗渲染函数
function renderCollaboratedDetails(creatorId) {
    const creator = checkCollaboratedData['data'].find(item => item.id === creatorId);
    if (!creator) return;

    // 设置创作者名称
    document.querySelector('.display-collaborated-details-box .creator-name').textContent = creator.nickname;

    // 渲染details日志
    const detailsUl = document.querySelector('.display-collaborated-details-box ul.details');
    detailsUl.innerHTML = '';
    creator.details.forEach(detail => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span class="update">${detail.update}</span>
            <span class="text">${detail.text}</span>
            <span class="has-collaborated">${detail.has_collaborated === "True" ? '已合作' : '未合作'}</span>
        `;
        detailsUl.appendChild(li);
    });

    // 渲染check日志
    const checkUl = document.querySelector('.display-collaborated-details-box ul.check');
    checkUl.innerHTML = '';
    creator.check.forEach(checkItem => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span class="update">${checkItem.update}</span>
            <span class="has-collaborated">${checkItem.has_collaborated === "True" ? '已合作' : '未合作'}</span>
        `;
        checkUl.appendChild(li);
    });
}
// 关闭弹窗逻辑
document.querySelector('.display-collaborated-details-mask-box .fork').addEventListener('click', hideCollaboratedDetails);
document.addEventListener('click', function(event) {
    if (!event.target.closest('.display-collaborated-details-box') && 
        !event.target.closest('.collaborated-data table svg')) {
        hideCollaboratedDetails();
    }
});

function hideCollaboratedDetails() {
    document.querySelector('.display-collaborated-details-mask-box').classList.remove('unhidden');
}

