# -*- coding: robot -*-

*** Settings ***
Library           OperatingSystem
Library           Collections
Library           Process
Library           DateTime

*** Variables ***
${HOST}   localhost
${UDP_URI}   udp://localhost:6002
${RTSP_URI}     rtsp://localhost:1235/file.rtsp
${FFSERVER}   ffserver -f ffserver.config
${UDP_BROADCAST}     gst-launch-1.0 -v filesrc location=SampleVideo_1280x720_5mb.mp4 ! decodebin ! x264enc ! rtph264pay ! udpsink host=localhost port=6002
#${UDP_BROADCAST}     gst-launch-1.0 -v v4l2src ! x264enc ! rtph264pay ! udpsink host=localhost port=6002
${TEST_UDP}     transform -u ${UDP_URI} -n 2000
${TEST_RTSP}     transform -u ${RTSP_URI} -n 2000

*** Test Cases ***
Set Up Dir    
    [Tags]    basic
    ${OUT_DIR}=    Create Out Dir
    Set Global Variable      ${OUT_DIR}

Start Udp Broadcast
    [Documentation]   Launch gstreamer
    [Tags]    udp broadcast
    ${CMD_RES}=    Start Process    ${UDP_BROADCAST}    shell=True	stdout=${TEMPDIR}/stdout.txt	stderr=${TEMPDIR}/stderr.txt
    #Log Many	stdout: ${CMD_RES.stdout}	stderr: ${CMD_RES.stderr}

Transform Udp Mp4
    [Documentation]   Run python script
    [Tags]    udp python mp4
    ${CMD_RES}=    Run Process    ${TEST_UDP} -o mp4 -d ${OUT_DIR}/udp_out.mp4   shell=True	timeout=1min  stdout=${TEMPDIR}/stdout.txt	stderr=${TEMPDIR}/stderr.txt
    Log Many	stdout: ${CMD_RES.stdout}	stderr: ${CMD_RES.stderr}
    Should Be Equal As Integers   ${CMD_RES.rc}   0
    File Should Exist    ${OUT_DIR}/udp_out.mp4
    File Should Not Be Empty    ${OUT_DIR}/udp_out.mp4

Transform Udp Frames
    [Documentation]   Run python script
    [Tags]    udp python jpeg
    ${CMD_RES}=    Run Process    ${TEST_UDP} -o frame -d ${OUT_DIR}/udp_out%00d.jpg   shell=True	timeout=1min  stdout=${TEMPDIR}/stdout.txt	stderr=${TEMPDIR}/stderr.txt
    Log Many	stdout: ${CMD_RES.stdout}	stderr: ${CMD_RES.stderr}
    Should Be Equal As Integers   ${CMD_RES.rc}   0
    File Should Exist    ${OUT_DIR}/udp_out0.jpg
    File Should Not Be Empty    ${OUT_DIR}/udp_out0.jpg

Stop Udp Broadcast
    [Tags]    udp broadcast
    Terminate All Processes

Start Rtsp Broadcast
    [Documentation]   Launch ffserver
    [Tags]    rtsp broadcast
    ${CMD_RES}=    Start Process    ${FFSERVER}    shell=True	stdout=${TEMPDIR}/stdout.txt	stderr=${TEMPDIR}/stderr.txt
    #Log Many	stdout: ${CMD_RES.stdout}	stderr: ${CMD_RES.stderr}
    
Transform Rtsp Mp4
    [Documentation]   Run python script
    [Tags]    rtsp python mp4
    ${CMD_RES}=    Run Process    ${TEST_RTSP} -o mp4 -d ${OUT_DIR}/rtsp_out.mp4   shell=True	timeout=1min  stdout=${TEMPDIR}/stdout.txt	stderr=${TEMPDIR}/stderr.txt
    Log Many	stdout: ${CMD_RES.stdout}	stderr: ${CMD_RES.stderr}
    Should Be Equal As Integers   ${CMD_RES.rc}   0
    File Should Exist    ${OUT_DIR}/rtsp_out.mp4
    File Should Not Be Empty    ${OUT_DIR}/rtsp_out.mp4

Transform Rtsp Frames
    [Documentation]   Run python script
    [Tags]    rtsp python jpeg
    ${CMD_RES}=    Run Process    ${TEST_RTSP} -o frame -d ${OUT_DIR}/rtsp_out%00d.jpg   shell=True	timeout=1min  stdout=${TEMPDIR}/stdout.txt	stderr=${TEMPDIR}/stderr.txt
    Log Many	stdout: ${CMD_RES.stdout}	stderr: ${CMD_RES.stderr}
    Should Be Equal As Integers   ${CMD_RES.rc}   0
    File Should Exist    ${OUT_DIR}/rtsp_out0.jpg
    File Should Not Be Empty    ${OUT_DIR}/rtsp_out0.jpg

Stop Rtsp Broadcast
    [Tags]    rtsp broadcast
    Terminate All Processes

*** Keywords ***
Create Out Dir
    ${TD}=    Get Current Date    result_format=%Y-%m-%d--%H-%M-%S
    Create Directory    out_${TD}
    [return]    out_${TD}
