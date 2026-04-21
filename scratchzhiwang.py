import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import csv
import os

os.chdir(r'C:\Users\lenovo\Desktop\CODE_Field\CODE_PY\exercise\研一\爬文献')

# 配置 Edge 选项
options = webdriver.EdgeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 30)  # 增加到30秒

try:
    print("="*70)
    print("知网 CSSCI 文献爬取工具")
    print("="*70)
    
    # 步骤1: 打开页面
    print("\n[1/8] 打开知网高级检索页面...")
    url = 'https://kns.cnki.net/kns8s/AdvSearch'
    driver.get(url)
    time.sleep(5)
    print("✓ 页面加载完成")
    
    # 步骤2: 点击检索输入栏
    print("\n[2/8] 准备输入检索条件...")
    try:
        search_click = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="ModuleSearch"]/div[2]/div/div/ul/li[1]/a/span')
        ))
        search_click.click()
        time.sleep(2)
    except:
        print("  (检索栏可能已展开)")
    
    # 步骤3: 输入关键词
    print("\n[3/9] 输入检索关键词 (区域创新 + 创新中心) * 现代化产业体系'...")
    input_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="gradetxt"]/dd[1]/div[2]/input')
    ))
    input_field.clear()
    input_field.send_keys("(区域创新 + 创新中心) * 现代化产业体系")
    time.sleep(2)
    print("✓ 关键词已输入")
    
    # 步骤4: 输入期刊名称
    print("\n[4/9] 输入期刊名称...")
    journal_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/div/dl/dd[3]/div[2]/input')
    ))
    journal_input.clear()
    journal_name = '经济学 + 中国工业经济 + 经济研究 + 数量经济技术经济研究 + 管理世界 + 管理科学学报 + 金融学报 + 中国社会科学 + 世界经济'  # 这里修改你要检索的期刊名称
    journal_input.send_keys(journal_name)
    time.sleep(2)
    print(f"✓ 期刊名称 '{journal_name}' 已输入")
    
    # 步骤5: 选中CSSCI
    print("\n[5/9] 选中 CSSCI 类论文...")
    cssci_checkbox = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div[2]/div[2]/div[3]/div/label[5]/input')
    ))
    
    driver.execute_script("arguments[0].scrollIntoView();", cssci_checkbox)
    time.sleep(1)
    
    if not cssci_checkbox.is_selected():
        cssci_checkbox.click()
        print("✓ CSSCI 已选中")
    else:
        print("✓ CSSCI 已经是选中状态")
    time.sleep(2)
    
    # 步骤6: 进行检索
    print("\n[6/9] 执行检索...")
    search_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div[2]/div[3]/div/input')
    ))
    search_button.click()
    print("  等待检索结果加载...")
    time.sleep(8)  # 增加等待时间
    
    # 保存检索后的截图
    driver.save_screenshot("after_search.png")
    print("✓ 检索完成（截图已保存: after_search.png）")
    
    # 步骤7: 显示详细信息
    print("\n[7/9] 切换到详细信息模式...")
    try:
        # 尝试多种可能的XPath
        detail_button = None
        xpaths = [
            '/html/body/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/ul[2]/li[1]/i',
            "//i[contains(@class, 'detail')]",
            "//li[@class='list-item']//i",
        ]
        
        for xpath in xpaths:
            try:
                detail_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                detail_button.click()
                time.sleep(3)
                print("✓ 已切换到详细模式")
                break
            except:
                continue
        
        if detail_button is None:
            print("  (可能已经是详细模式，或按钮不存在)")
            
    except Exception as e:
        print(f"  详细模式切换失败: {e}")
        print("  继续执行...")
    
    # 步骤8: 修改每页显示50条
    print("\n[8/9] 设置每页显示50条...")
    try:
        page_dropdown = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="perPageDiv"]/div/i')
        ))
        page_dropdown.click()
        time.sleep(1)
        
        option_50 = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="perPageDiv"]/ul/li[3]/a')
        ))
        option_50.click()
        time.sleep(6)
        print("✓ 已设置为每页50条")
    except Exception as e:
        print(f"  无法修改显示条数: {e}")
        print("  使用默认显示条数继续...")
    
    # 步骤9: 开始爬取数据
    print("\n[9/9] 开始爬取文献数据...")
    print("-"*70)
    
    # 调试：查看页面上有哪些元素
    print("\n【调试信息】检查页面结构...")
    try:
        # 尝试多种可能的定位方式
        possible_selectors = [
            '//*[@id="gridTable"]/div/div/dl/dd',
            '//div[@id="gridTable"]//dd',
            '//table[@id="gridTable"]//tr',
            '//div[contains(@class,"result")]//dd',
            '//div[@class="result-table-list"]//dd',
        ]
        
        found = False
        for selector in possible_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if len(elements) > 0:
                    print(f"  ✓ 找到 {len(elements)} 个元素（使用: {selector}）")
                    found = True
                    break
            except:
                continue
        
        if not found:
            print("  ✗ 未找到文献列表元素")
            print("\n  尝试查找页面上的所有 dd 元素...")
            all_dd = driver.find_elements(By.TAG_NAME, "dd")
            print(f"  页面共有 {len(all_dd)} 个 dd 元素")
            
            # 保存页面源码供调试
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("  页面源码已保存到: page_source.html")
            
            driver.save_screenshot("debug_page.png")
            print("  页面截图已保存到: debug_page.png")
            
            print("\n  请检查以下内容:")
            print("  1. 查看 after_search.png 确认是否成功进入结果页面")
            print("  2. 查看 debug_page.png 确认当前页面状态")
            print("  3. 检查是否有验证码或登录要求")
            print("  4. 打开 page_source.html 查找文献列表的实际结构")
            
            raise Exception("无法定位文献列表元素")
            
    except Exception as e:
        print(f"\n  调试检查出错: {e}")
        raise
    
    all_data = []
    page_num = 1
    max_pages = 20
    
    # 使用找到的正确选择器
    result_selector = selector  # 从上面的循环中获得
    
    while page_num <= max_pages:
        print(f"\n正在爬取第 {page_num} 页...")
        
        try:
            # 等待页面加载
            wait.until(EC.presence_of_element_located((By.XPATH, result_selector)))
            time.sleep(3)
            
            # 获取当前页所有文献条目
            elements = driver.find_elements(By.XPATH, result_selector)
            print(f"  本页共 {len(elements)} 条记录")
            
            # 遍历每条记录
            for i in range(1, len(elements) + 1):
                row_data = []
                
                # 尝试多种XPath模式
                title_xpaths = [
                    f'{result_selector}[{i}]/div[2]/h6/a',
                    f'{result_selector}[{i}]//h6/a',
                    f'{result_selector}[{i}]//a[@class="fz14"]',
                ]
                
                # 1. 文章题目
                for xpath in title_xpaths:
                    try:
                        title = driver.find_element(By.XPATH, xpath).text.strip()
                        if title:
                            row_data.append(title)
                            break
                    except:
                        continue
                else:
                    row_data.append("NA")
                
                # 2. 第一作者
                try:
                    author = driver.find_element(
                        By.XPATH, 
                        f'{result_selector}[{i}]//div[@class="author"]//a'
                    ).text.strip()
                    row_data.append(author)
                except:
                    try:
                        author = driver.find_element(
                            By.XPATH, 
                            f'{result_selector}[{i}]/div[2]/div/p/a'
                        ).text.strip()
                        row_data.append(author)
                    except:
                        row_data.append("NA")
                
                # 3. 单位
                try:
                    institution = driver.find_element(
                        By.XPATH, 
                        f'{result_selector}[{i}]/div[2]/div/p/span/a'
                    ).text.strip()
                    row_data.append(institution)
                except:
                    row_data.append("NA")
                
                # 4. 期刊
                try:
                    journal = driver.find_element(
                        By.XPATH, 
                        f'{result_selector}[{i}]/div[2]/p[1]/span[1]/a'
                    ).text.strip()
                    row_data.append(journal)
                except:
                    row_data.append("NA")
                
                # 5. 关键词
                try:
                    keywords = driver.find_element(
                        By.XPATH, 
                        f'{result_selector}[{i}]/div[2]/p[3]'
                    ).text.strip()
                    row_data.append(keywords)
                except:
                    row_data.append("NA")
                
                all_data.append(row_data)
                
                if len(all_data) % 10 == 0:
                    print(f"  已爬取 {len(all_data)} 条...")
            
            print(f"  第 {page_num} 页完成，累计 {len(all_data)} 条")
            
            # 尝试翻页
            try:
                next_button = driver.find_element(By.ID, 'PageNext')
                
                if 'disabled' in next_button.get_attribute('class') or not next_button.is_enabled():
                    print(f"\n已到最后一页（第 {page_num} 页）")
                    break
                
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(1)
                next_button.click()
                time.sleep(5)
                page_num += 1
                
            except NoSuchElementException:
                print("\n没有找到下一页按钮")
                break
                
        except TimeoutException:
            print(f"  第 {page_num} 页加载超时")
            break
        except Exception as e:
            print(f"  第 {page_num} 页出错: {e}")
            break
    
    # 保存到CSV
    print("\n" + "="*70)
    print("保存数据到CSV文件...")
    
    with open("区域生态1.csv", "w", newline="", encoding='utf_8_sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['标题', '第一作者', '单位', '期刊', '关键词'])
        writer.writerows(all_data)
    
    print(f"✓ 爬取完成！")
    print(f"  - 共爬取 {len(all_data)} 条文献记录")
    print(f"  - 已保存到: 页面元素.csv")
    print("="*70)

except TimeoutException as e:
    print("\n✗ 页面元素加载超时")
    print(f"详细信息: {e}")
    print("建议: 检查网络连接或手动打开网页确认是否需要登录")
    
except Exception as e:
    print(f"\n✗ 发生错误: {e}")
    import traceback
    traceback.print_exc()
    
    try:
        driver.save_screenshot("error_screenshot.png")
        print("已保存错误截图: error_screenshot.png")
    except:
        pass

finally:
    print("\n关闭浏览器...")
    driver.quit()
    print("完成！")