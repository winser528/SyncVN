#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import argparse
import sys


def m3u_to_json(m3u_file_path, output_file=None):
    """
    将M3U文件转换为JSON格式
    Args:
        m3u_file_path (str): M3U文件路径
        output_file (str): 输出JSON文件路径，如果为None则输出到控制台
    """
    try:
        # 读取M3U文件
        with open(m3u_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        channels = []
        channel_num = 1
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # 跳过空行和注释行（以#EXTM3U开头的行）
            if not line or line.startswith('#EXTM3U'):
                i += 1
                continue
            # 处理频道信息行（以#EXTINF开头的行）
            if line.startswith('#EXTINF'):
                channel_info = parse_extinf_line(line)
                # 下一行应该是URL
                if i + 1 < len(lines):
                    url_line = lines[i + 1].strip()
                    if url_line and not url_line.startswith('#') and url_line.startswith('http'):
                        channel = {
                            "channelNum": channel_num,
                            "channelName": channel_info.get('name', ''),
                            "channelUrl": url_line,
                            "channelLogo": channel_info.get('logo', '')
                        }
                        channels.append(channel)
                        channel_num += 1
                    i += 2  # 跳过URL行
                    continue
            else:
                i += 1
        # 输出结果
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(channels, f, ensure_ascii=False, indent=4)
            print(f"转换完成！共转换 {len(channels)} 个频道，结果已保存到 {output_file}")
        else:
            print(json.dumps(channels, ensure_ascii=False, indent=4))
        return channels
    except Exception as e:
        print(f"转换过程中出现错误: {e}")
        return None


def parse_extinf_line(extinf_line):
    """
    解析#EXTINF行，提取频道名称和logo信息
    Args:
        extinf_line (str): #EXTINF行内容
    Returns:
        dict: 包含频道信息的字典
    """
    info = {'name': '', 'logo': ''}
    try:
        # 匹配格式：#EXTINF:-1 tvg-id="..." tvg-name="..." tvg-logo="..." group-title="...",频道名称
        pattern = r'#EXTINF:-1[^,]*,(.+)'
        match = re.search(pattern, extinf_line)
        if match:
            info['name'] = match.group(1).strip()
        # 提取logo信息
        logo_pattern = r'tvg-logo="([^"]*)"'
        logo_match = re.search(logo_pattern, extinf_line)
        if logo_match:
            info['logo'] = logo_match.group(1)
    except Exception as e:
        print(f"解析EXTINF行时出错: {e}")

    return info


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 如果直接运行，可以使用示例
        # 示例用法：
        # python m3u_to_json.py input.m3u -o output.json
        parser = argparse.ArgumentParser(description='将M3U文件转换为JSON格式')
        parser.add_argument('input_file', help='输入的M3U文件路径')
        parser.add_argument('-o', '--output', help='输出的JSON文件路径')
        args = parser.parse_args()
        # 检查输入文件是否存在
        if not os.path.exists(args.input_file):
            print(f"错误：文件 {args.input_file} 不存在")
        else:
            m3u_to_json(args.input_file, args.output)
    else:
        m3u_to_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'iptv.m3u'), 'liveChannel.json')
