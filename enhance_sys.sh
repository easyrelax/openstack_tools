# SSH���
mkdir -p /tmp/backup
cp /etc/ssh/sshd_config /tmp/backup

sed -i 's/#LogLevel INFO/LogLevel VERBOSE/' /etc/ssh/sshd_config
sed -i 's/#PermitEmptyPasswords/PermitEmptyPasswords/' /etc/ssh/sshd_config
sed -i 's/#StrictModes/StrictModes/' /etc/ssh/sshd_config

# ���ÿ�ݼ�
cp /usr/lib/systemd/system/ctrl-alt-del.target /tmp/backup
rm -f /usr/lib/systemd/system/ctrl-alt-del.target

# ��ʱ�Ự�ǳ�
cp /etc/profile /tmp/backup
cat /etc/profile | grep TMOUT || echo -e 'TMOUT=300\nexport TMOUT' >> /etc/profile
source /etc/profile

# ����ħ����
cp /etc/sysctl.conf /tmp/backup
echo "kernel.sysrq=0" >> /etc/sysctl.conf
sysctl -p


# ��¼��ȫ��ǿ
# ����
cp  /etc/pam.d/password-auth /tmp/backup
cp  /etc/pam.d/system-auth /tmp/backup
cp  /etc/security/pwquality.conf /tmp/backup

# ����/etc/pam.d/password-auth����
sed -i '4aauth        required      pam_tally2.so preauth silent audit deny=3 even_deny_root unlock_time=300 root_unlock_time=300' /etc/pam.d/password-auth
sed -i '9aaccount        required     pam_faillock.so' /etc/pam.d/password-auth
sed -i 's@password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 authtok_type=@password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 authtok_type= enforce_for_root@g' /etc/pam.d/password-auth

# ����/etc/pam.d/system-auth����
sed -i '4aauth        required      pam_tally2.so preauth silent audit deny=3 even_deny_root unlock_time=300 root_unlock_time=300'  /etc/pam.d/system-auth
sed -i '9aaccount     required      pam_faillock.so'  /etc/pam.d/system-auth
sed -i 's@password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 authtok_type=@password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 authtok_type= enforce_for_root@g'   /etc/pam.d/system-auth

# ����/etc/security/pwquality.conf����
sed -i "/minlen/c"minlen\ =\ 8"" /etc/security/pwquality.conf
sed -i "/dcredit/c"dcredit\ =\ -1"" /etc/security/pwquality.conf
sed -i "/ucredit/c"ucredit\ =\ -1"" /etc/security/pwquality.conf
sed -i "/lcredit/c"lcredit\ =\ -1"" /etc/security/pwquality.conf
sed -i "/ocredit/c"ocredit\ =\ -1"" /etc/security/pwquality.conf

# ����sshd����
systemctl restart sshd


# �����û�������Ч��ֹʱ��
cp /etc/login.defs /tmp/backup
sed -i "/^PASS_MAX_DAYS/c"PASS_MAX_DAYS\ \ \ 90"" /etc/login.defs
sed -i "/^PASS_WARN_AGE/c"PASS_WARN_AGE\ \ \ 7"" /etc/login.defs


# �޸�keystone
mkdir -p /tmp/backup_keystone
cp /etc/keystone/keystone-paste.ini /tmp/backup_keystone
sed -i 's/use = egg:keystone#admin_token_auth/#use = egg:keystone#admin_token_auth/' /etc/keystone/keystone-paste.ini
sed -i 's/request_id\ admin_token_auth/request_id/g' /etc/keystone/keystone-paste.ini
systemctl restart openstack-keystone.service
